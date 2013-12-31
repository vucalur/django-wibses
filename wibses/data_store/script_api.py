import json
from multiprocessing.synchronize import Lock
import shutil
import threading
import datetime
import time
import re
import ConfigParser
import os
import git
from gitdb.exc import BadObject
from repoze.lru import lru_cache

from wibses import JSON_INDENT
from wibses.data_store import REQUEST_PARAM_NAME__USER, JSON_ATTR_NAME__REVISION, \
    JSON_ATTR_NAME__MODIFIED_DATE, JSON_ATTR_NAME__CHANGER, STORAGE_DEFAULT_SCAN_PERIOD_MS, \
    DEFAULT_STORAGE_SCRIPT_CREATOR_NAME, STORAGE_ID_GENERATOR_POSITIONS_COUNT, JSON_ATTR_NAME__PARAMS, \
    JSON_ATTR_NAME__NAME, JSON_ATTR_SCRIPT_ID, JSON_ATTR_NAME__ID, REPO_CONF_FILENAME, \
    REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP, REPO_CONF_SECTION__SCRIPT_INFO, TIMESTAMP_FORMAT
from wibses.data_store.exceptions import NoSuchScriptInStorageException, BadScriptRevisionException
from wibses.data_store.validation import get_semantic_validator
from wibses.utils import get_folder_containing_names, merge_into_path, get_script_id_for_repo_dir_name, \
    get_repo_dir_name_for_script_id, CombinationsGenerator, read_script_object, write_script_object, dump_json
from wibses.data_store import REPO_GITIGNORE_FILENAME, REPO_IGNORED_FILENAMES


class ScriptManagerNotInitializedException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, args, kwargs)


def synchronized(function, *args, **kwargs):
    def decorator(*args, **kwargs):
        try:
            args[0].get_lock().acquire()
            k = function(*args, **kwargs)
        finally:
            args[0].get_lock().release()
        return k

    return decorator


class Script:
    def __init__(self,
                 scripts_storage_path,
                 script_id=None,
                 script_repo_dir=None,
                 storage_filename_with_ext=None,
                 creator_name=DEFAULT_STORAGE_SCRIPT_CREATOR_NAME,
                 create_from_existing_repo=False):

        if create_from_existing_repo:
            assert not script_repo_dir is None
        else:
            assert not script_id is None
            assert not storage_filename_with_ext is None

        self._script_id = script_id
        self._repo_file_name = str(script_id) + '.json'

        self._repo_dir_path = None
        self._repo_file_path = None
        self._repo = None
        self._storage_file_path = None
        self._script_text = None
        self._script_obj = None
        self._name = None
        self._storage_file_name = storage_filename_with_ext

        if create_from_existing_repo:
            self.__create_from_repo(scripts_storage_path, script_repo_dir)
        else:
            self.__create_from_storage_file(scripts_storage_path, storage_filename_with_ext)

        self._modification_info = ScriptModificationInfo(self,
                                                         fresh_info=not create_from_existing_repo,
                                                         creator_name=creator_name)

    def __create_from_repo(self, storage_path, repo_dir):
        self._repo_dir_path = merge_into_path([storage_path, repo_dir])

        self._script_id = get_script_id_for_repo_dir_name(repo_dir)
        self._repo_file_name = self._script_id + '.json'
        self._repo_file_path = merge_into_path([self._repo_dir_path, self._repo_file_name])

        self.load_script_from_repo()

        self._script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__ID] = self._script_id
        self._repo = git.Repo(self._repo_dir_path)

        active_filename = self._repo_file_name
        try:
            conf_file_fp = open(merge_into_path([self._repo_dir_path, REPO_CONF_FILENAME]), 'r')
            configuration = ConfigParser.ConfigParser()
            configuration.readfp(conf_file_fp)
            active_filename = configuration.get(REPO_CONF_SECTION__SCRIPT_INFO,
                                                REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP)
            conf_file_fp.close()
        except Exception:
            pass

        self._storage_file_path = merge_into_path([storage_path, active_filename])
        self._storage_file_name = active_filename
        self._copy_from_repo_to_storage()

    def __create_from_storage_file(self, storage_path, storage_filename_with_ext):
        self._repo_dir_path = merge_into_path([storage_path, get_repo_dir_name_for_script_id(self._script_id)])

        self._repo_file_path = merge_into_path([self._repo_dir_path, self._repo_file_name])
        self._storage_file_path = merge_into_path([storage_path, storage_filename_with_ext])

        if not os.path.exists(self._repo_dir_path):
            os.mkdir(self._repo_dir_path)
        # create .gitignore file
        gi_fp = open(merge_into_path([self._repo_dir_path, REPO_GITIGNORE_FILENAME]), 'w')
        try:
            for ignored_file_name in REPO_IGNORED_FILENAMES:
                gi_fp.write(ignored_file_name + '\n')
        finally:
            gi_fp.close()
        #create repo info file
        repo_cfg_file_text = "[%s]\n%s = %s\n" % (REPO_CONF_SECTION__SCRIPT_INFO,
                                                  REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP,
                                                  storage_filename_with_ext)

        repo_cfg_file_fp = open(merge_into_path([self._repo_dir_path, REPO_CONF_FILENAME]), "w")
        try:
            repo_cfg_file_fp.write(repo_cfg_file_text)
        finally:
            repo_cfg_file_fp.close()

        self._repo = git.Repo.init(self._repo_dir_path)
        self._copy_from_storage_to_repo()
        self.load_script_from_repo()

    def get_modification_info(self):
        return self._modification_info

    def get_id(self):
        return self._script_id

    def get_name(self):
        return self._name

    def get_json(self):
        return dump_json(self._script_obj, JSON_INDENT)

    def load_script_from_repo(self):
        s_file = open(self._repo_file_path, "r")
        try:
            script_text = s_file.read().replace("\n", "")
        finally:
            s_file.close()
        self._script_obj = json.loads(script_text)
        self._script_text = script_text
        self._name = self._script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__NAME]

    def get_history_json(self):
        return self._modification_info.get_history()

    def update(self, body_text, changer_username):

        get_semantic_validator().validate_script(body_text)

        self._script_obj = json.loads(body_text)
        self._script_text = body_text
        self._name = self._script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__NAME]

        self.__update_script_file(body_text, self._repo_file_path)
        self._copy_from_repo_to_storage()
        self._modification_info.update_modification(changer_username)

    @lru_cache(maxsize=50)
    def get_revision(self, revision_hash):
        try:
            commit = self._repo.commit(revision_hash)
            script_text = commit.tree[self._repo_file_name].data_stream.read().replace("\n", "")

            script_json = json.loads(script_text)
            return dump_json(script_json, JSON_INDENT)
        except BadObject:
            raise BadScriptRevisionException(revision_hash)

    def delete(self):
        if os.path.exists(self._storage_file_path):
            shutil.rmtree(self._storage_file_path)
        if os.path.exists(self._repo_dir_path):
            shutil.rmtree(self._repo_dir_path)

    def _copy_from_repo_to_storage(self):
        shutil.copy(self._repo_file_path, self._storage_file_path)

    def _copy_from_storage_to_repo(self):
        shutil.copy(self._storage_file_path, self._repo_file_path)

    def __update_script_file(self, script_text, script_file_path):
        f = open(script_file_path, "w")
        try:
            f.write(script_text)
        finally:
            f.close()


#Creates commit of newly created script file (if is fresh)
class ScriptModificationInfo:
    def __init__(self, script, creator_name, fresh_info=True):
        self._last_changer = None
        self._last_modification_date = None

        self._history_list = list()

        assert isinstance(script, Script)
        self._parent_script = script

        if fresh_info:
            self.update_modification(creator_name)
        else:
            self.__load_history()

    def __update_modification_date(self):
        self._last_modification_date = datetime.datetime.fromtimestamp(time.time()).strftime(TIMESTAMP_FORMAT)

    def __load_history(self):
        repo = self._parent_script._repo
        for commit in repo.iter_commits():
            commit_timestamp = datetime.datetime.fromtimestamp(commit.committed_date)
            commit_date_str = commit_timestamp.strftime(TIMESTAMP_FORMAT)

            update_info_string_raw = commit.message
            update_info_string = re.search(r'\{.*\}', update_info_string_raw).group(0)
            revision_hash = commit.name_rev.split()[0]

            hist_attributes = json.loads(update_info_string.replace("'", '"'))
            user_name = hist_attributes[REQUEST_PARAM_NAME__USER]

            self._history_list.append({
                JSON_ATTR_NAME__REVISION: revision_hash,
                JSON_ATTR_NAME__MODIFIED_DATE: commit_date_str,
                JSON_ATTR_NAME__CHANGER: user_name
            })
        self._last_changer = self._history_list[0][JSON_ATTR_NAME__CHANGER]
        self._last_modification_date = self._history_list[0][JSON_ATTR_NAME__MODIFIED_DATE]

    def sort_key(self):
        return self._parent_script._name

    def encode(self):
        return {
            JSON_ATTR_NAME__CHANGER: self._last_changer,
            JSON_ATTR_NAME__MODIFIED_DATE: self._last_modification_date,
            JSON_ATTR_NAME__NAME: self._parent_script._name,
            JSON_ATTR_SCRIPT_ID: self._parent_script._script_id
        }

    def get_history(self):
        return dump_json(self._history_list, JSON_INDENT)

    def update_modification(self, changer):
        self._last_changer = changer
        self.__update_modification_date()

        commit_msg = "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER, changer)

        repo = self._parent_script._repo

        repo.git.add(self._parent_script._repo_file_name)
        repo.git.commit(m=commit_msg)

        for c in repo.iter_commits():
            self._history_list = [{
                JSON_ATTR_NAME__REVISION: c.name_rev.split()[0],
                JSON_ATTR_NAME__MODIFIED_DATE: self._last_modification_date,
                JSON_ATTR_NAME__CHANGER: changer
            }] + self._history_list
            break


class StorageDaemon(threading.Thread):
    def __init__(self, checking_period_ms, script_manager):
        threading.Thread.__init__(self)
        self._sleep_per_in_seconds = checking_period_ms / 1000.0

        assert isinstance(script_manager, ScriptManager)
        self._script_manager = script_manager

        self._stop = False
        self._checked_file_paths = set()
        self.daemon = True

    def get_lock(self):
        return self._script_manager.get_lock()

    def run(self):

        while not self._stop:
            self.do_work()
            time.sleep(self._sleep_per_in_seconds)

    @synchronized
    def do_work(self):
        file_names = get_folder_containing_names(self._script_manager._script_storage_path, incl_file_names=True)
        patt = r'(.+)\.json'
        script_names_without_ext = set(map(lambda x: re.search(patt, x).group(1),
                                           filter(lambda x: re.search(patt, x) is not None,
                                                  file_names)))
        scripts_names_with_ext = map(lambda x: x + '.json', script_names_without_ext)

        manager_scripts = self._script_manager._scripts_dict

        for script_filename in scripts_names_with_ext:
            script_candidate_path = merge_into_path([
                self._script_manager._script_storage_path,
                script_filename
            ])

            if script_candidate_path not in self._checked_file_paths:
                try:
                    script_obj = read_script_object(script_candidate_path)
                    if get_semantic_validator().validate_script(script_obj, is_text=False, with_raise=False):
                        if not script_filename in self._script_manager._script_id_by_storage_filename:
                            script_id = self._script_manager.unsynch__get_free_script_id()
                            new_script = Script(self._script_manager._script_storage_path,
                                                script_id=script_id,
                                                storage_filename_with_ext=script_filename,
                                                create_from_existing_repo=False)
                            manager_scripts[script_id] = new_script
                            self._script_manager._script_id_by_storage_filename[script_filename] = script_id
                except Exception:
                    pass
                self._checked_file_paths.add(script_candidate_path)

        to_clean = []

        for registered_script_filename in self._script_manager._script_id_by_storage_filename:
            if registered_script_filename not in scripts_names_with_ext:
                to_clean.append(registered_script_filename)

        for removed_script_file_name in to_clean:
            script_id = self._script_manager._script_id_by_storage_filename[removed_script_file_name]

            script = manager_scripts[script_id]
            script.delete()

            del self._script_manager._scripts_dict[script_id]
            del self._script_manager._script_id_by_storage_filename[removed_script_file_name]
            self._checked_file_paths.remove(script._storage_file_path)


class ScriptManager:
    def __init__(self, script_storage_path, storage_checker_period):
        self._script_storage_path = script_storage_path

        self._scripts_dict = dict()
        self._script_id_by_storage_filename = dict()

        self._storage_operations_lock = Lock()
        self._storage_daemon = StorageDaemon(storage_checker_period, self)

        self.__script_id_generator = CombinationsGenerator(STORAGE_ID_GENERATOR_POSITIONS_COUNT)

        inner_dirs = get_folder_containing_names(script_storage_path, incl_dir_names=True)

        for repo_candidate_dir in inner_dirs:
            candidate_path = merge_into_path([script_storage_path, repo_candidate_dir])
            candidate_inner_dirs = get_folder_containing_names(candidate_path, incl_dir_names=True)
            if ".git" in candidate_inner_dirs:
                new_script = Script(self._script_storage_path,
                                    script_repo_dir=repo_candidate_dir,
                                    create_from_existing_repo=True)
                script_id = new_script._script_id
                self._scripts_dict[script_id] = new_script
                self._script_id_by_storage_filename[new_script._storage_file_name] = script_id

        self._storage_daemon.start()

    #OK
    @synchronized
    def get_scripts_in_storage_json(self):
        result = list()

        for script in self._scripts_dict.values():
            result.append(script.get_modification_info())
        result.sort(key=lambda x: x.sort_key())
        result = map(lambda x: x.encode(), result)

        return dump_json(result, JSON_INDENT)

    #OK
    @synchronized
    def update_script_in_storage(self, script_id, script_body, changer_username):
        if script_id not in self._scripts_dict:
            raise NoSuchScriptInStorageException(script_id)

        script = self._scripts_dict[script_id]
        script.update(script_body, changer_username)

    #OK
    @synchronized
    def get_script_history_json(self, script_id):
        if script_id not in self._scripts_dict:
            raise NoSuchScriptInStorageException(script_id)

        script = self._scripts_dict[script_id]
        return script.get_history_json()

    #OK
    @synchronized
    def get_script(self, script_id):
        try:
            script = self._scripts_dict[script_id]
            return script.get_json()
        except Exception:
            raise NoSuchScriptInStorageException(script_id)

    #OK
    @synchronized
    def get_script_revision(self, script_id, revision_hash):
        if script_id not in self._scripts_dict:
            raise NoSuchScriptInStorageException(script_id)

        script = self._scripts_dict[script_id]
        return script.get_revision(revision_hash)

    #OK
    @synchronized
    def create_script_in_repo(self, creator_name, storage_filename):
        result_json = self.__unsynch__create_script_in_repo(creator_name, st_filename=storage_filename)
        return result_json

    @synchronized
    def fork_script_of_revision(self, script_id, revision_hash, creator_name, storage_filename):
        if script_id not in self._scripts_dict:
            raise NoSuchScriptInStorageException(script_id)

        script = self._scripts_dict[script_id]
        json_to_fork = script.get_revision(revision_hash)

        result_json = self.__unsynch__create_script_in_repo(creator_name,
                                                            script_text=json_to_fork,
                                                            st_filename=storage_filename)
        return result_json

    def __unsynch__create_script_in_repo(self, creator_name, script_text=None, st_filename=None):
        script_id = self.unsynch__get_free_script_id()

        if st_filename is None:
            st_filename = script_id
        elif st_filename.endswith(".json"):
            st_filename = st_filename[0:st_filename.index(".json")]

        counter = 1
        begin_name = st_filename
        while True:
            if not os.path.exists(merge_into_path([self._script_storage_path, st_filename + ".json"])):
                break
            st_filename = "%s(%d)" % (begin_name, counter)
            counter += 1

        if script_text is None:
            new_script_obj = get_semantic_validator().get_script_template()
        else:
            new_script_obj = json.loads(script_text)

        new_script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__ID] = script_id

        storage_file_name_with_ext = st_filename + ".json"

        script_in_storage_path = merge_into_path([self._script_storage_path, storage_file_name_with_ext])
        write_script_object(script_in_storage_path, new_script_obj)

        new_script = Script(self._script_storage_path,
                            script_id=script_id,
                            storage_filename_with_ext=storage_file_name_with_ext,
                            creator_name=creator_name,
                            create_from_existing_repo=False)

        self._scripts_dict[script_id] = new_script
        self._script_id_by_storage_filename[storage_file_name_with_ext] = script_id

        return dump_json(new_script_obj, JSON_INDENT)

    def unsynch__get_free_script_id(self):
        script_id = self.__script_id_generator.next_combination()

        while script_id in self._scripts_dict:
            script_id = self.__script_id_generator.next_combination()

        return script_id

    def get_lock(self):
        return self._storage_operations_lock


class ScriptUtils:
    __script_storage_manager = None
    __script_storage_path = None
    __script_storage_checking_period = STORAGE_DEFAULT_SCAN_PERIOD_MS

    @staticmethod
    def set_scripts_storage_path(storage_path):
        ScriptUtils.__script_storage_path = storage_path

    @staticmethod
    def set_store_scan_period_in_ms(new_period):
        ScriptUtils.__script_storage_checking_period = new_period

    @staticmethod
    def initialize():
        if ScriptUtils.__script_storage_manager is None and (ScriptUtils.__script_storage_path is not None):
            ScriptUtils.__script_storage_manager = ScriptManager(ScriptUtils.__script_storage_path,
                                                                 ScriptUtils.__script_storage_checking_period)

    @staticmethod
    def get_manager():
        man = ScriptUtils.__script_storage_manager
        if man is None:
            raise ScriptManagerNotInitializedException()
        assert isinstance(man, ScriptManager)
        return man