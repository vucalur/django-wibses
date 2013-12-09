import json
from multiprocessing.synchronize import Lock
import signal
import shutil
import threading
import datetime
from gitdb.exc import BadObject
import time
import re
import ConfigParser
import os


from wibses.data_store import JSON_INDENT, REQUEST_PARAM_NAME__USER, JSON_ATTR_NAME__REVISION, \
    JSON_ATTR_NAME__MODIFIED_DATE, JSON_ATTR_NAME__CHANGER, STORAGE_DEFAULT_SCAN_PERIOD_MS, \
    DEFAULT_STORAGE_SCRIPT_CREATOR_NAME, STORAGE_ID_GENERATOR_POSITIONS_COUNT, JSON_ATTR_NAME__PARAMS, \
    JSON_ATTR_NAME__NAME, JSON_ATTR_SCRIPT_ID, JSON_ATTR_NAME__ID, REPO_CONF_FILENAME, \
    REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP, REPO_CONF_SECTION__SCRIPT_INFO, TIMESTAMP_FORMAT
from wibses.data_store.exceptions import NoSuchScriptInStorageException, BadScriptRevisionException
from wibses.data_store.repo_management import get_repo_for_script, list_script_history, \
    get_particular_script_version, create_repo_for_script, update_script_in_repo
from wibses.data_store.validation import get_semantic_validator
from wibses.utils import get_folder_containing_names, merge_into_path, get_script_file_name_from_repo_dir_name, \
    get_repo_dir_name_for_script_filename, ASCIIdGenerator, read_script_object, write_script_object


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
        manager_scripts = self._script_manager._repositories_by_script_id
        for script_filename in script_names_without_ext:
            script_candidate_path = merge_into_path([
                self._script_manager._script_storage_path,
                script_filename + ".json"
            ])

            if script_candidate_path not in self._checked_file_paths:
                try:
                    script_obj = read_script_object(script_candidate_path)
                    if get_semantic_validator().validate_script(script_obj, is_text=False, with_raise=False):
                        s_par_dict = script_obj[JSON_ATTR_NAME__PARAMS]
                        if not (JSON_ATTR_NAME__ID in s_par_dict and
                                s_par_dict[JSON_ATTR_NAME__ID] in manager_scripts):
                            script_id = self._script_manager.unsynch_get_free_script_id()

                            script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__ID] = script_id
                            script_name = script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__NAME]
                            when_changed = datetime.datetime.fromtimestamp(time.time()).strftime(TIMESTAMP_FORMAT)

                            self._script_manager._scripts_modification_info_by_id[script_id] = {
                                JSON_ATTR_NAME__CHANGER: DEFAULT_STORAGE_SCRIPT_CREATOR_NAME,
                                JSON_ATTR_NAME__MODIFIED_DATE: when_changed,
                                JSON_ATTR_NAME__NAME: script_name,
                                JSON_ATTR_SCRIPT_ID: script_id
                            }

                            write_script_object(script_candidate_path, script_obj)

                            script_path = merge_into_path([self._script_manager._script_storage_path,
                                                           get_repo_dir_name_for_script_filename(script_id),
                                                           script_id + ".json"])
                            self._script_manager._script_repo_file_path_by_id[script_id] = script_path
                            self._script_manager._script_id_by_original_filename[script_filename + '.json'] = script_id
                            repo = create_repo_for_script(self._script_manager._script_storage_path,
                                                          script_filename_with_ext=script_filename + '.json',
                                                          script_id=script_id)
                            shutil.copyfile(script_candidate_path, script_path)

                            update_script_in_repo(repo, script_id + ".json",
                                                  "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER,
                                                                   DEFAULT_STORAGE_SCRIPT_CREATOR_NAME))

                            self._script_manager._repositories_by_script_id[script_id] = repo
                            self._script_manager._script_storage_file_path_by_id[script_id] = script_candidate_path

                except Exception:
                    pass
                self._checked_file_paths.add(script_candidate_path)

        storage_filenames_with_ext = set(map(lambda x: str(x) + '.json', script_names_without_ext))
        iteration_list = list(self._script_manager._script_id_by_original_filename.keys())

        for registered_script_filename in iteration_list:
            if registered_script_filename not in storage_filenames_with_ext:
                script_id = self._script_manager._script_id_by_original_filename[registered_script_filename]
                removed_script_file_path = merge_into_path([self._script_manager._script_storage_path,
                                                            registered_script_filename])
                self._checked_file_paths.remove(removed_script_file_path)
                del self._script_manager._repositories_by_script_id[script_id]
                del self._script_manager._scripts_modification_info_by_id[script_id]
                del self._script_manager._script_id_by_original_filename[registered_script_filename]
                del self._script_manager._script_repo_file_path_by_id[script_id]
                del self._script_manager._script_storage_file_path_by_id[script_id]

                script_repo_path = merge_into_path([
                    self._script_manager._script_storage_path,
                    get_repo_dir_name_for_script_filename(script_id)
                ])

                shutil.rmtree(script_repo_path, True)


class ScriptManager:
    def __init__(self, script_storage_path, storage_checker_period, script_template_filename):
        self._script_storage_path = script_storage_path
        self._repositories_by_script_id = {}
        self._scripts_modification_info_by_id = {}
        self._script_storage_file_path_by_id = {}
        self._script_repo_file_path_by_id = {}
        self._script_id_by_original_filename = {}
        self._storage_operations_lock = Lock()

        self._storage_daemon = StorageDaemon(storage_checker_period, self)
        self._template_script_object = json.loads(open(script_template_filename, "r").read().replace("\n", ""))
        self.__script_id_generator = ASCIIdGenerator(STORAGE_ID_GENERATOR_POSITIONS_COUNT)

        inner_dirs = get_folder_containing_names(script_storage_path, incl_dir_names=True)

        for repo_candidate_dir in inner_dirs:
            candidate_path = merge_into_path([script_storage_path, repo_candidate_dir])
            candidate_inner_dirs, candidate_inner_files = get_folder_containing_names(candidate_path,
                                                                                      incl_dir_names=True,
                                                                                      incl_file_names=True)
            if ".git" in candidate_inner_dirs:
                script_file_name = get_script_file_name_from_repo_dir_name(repo_candidate_dir)
                script_file_name_with_ext = script_file_name + ".json"
                script_source_path = merge_into_path([self._script_storage_path,
                                                      repo_candidate_dir,
                                                      script_file_name_with_ext])

                try:
                    script_obj = read_script_object(script_source_path)

                    if get_semantic_validator().validate_script(script_obj, is_text=False, with_raise=False):
                        script_name = script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__NAME]
                        script_id = script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__ID]

                        self._script_repo_file_path_by_id[script_id] = script_source_path
                        repo = get_repo_for_script(script_storage_path, script_file_name)
                        self._repositories_by_script_id[script_id] = repo

                        last_changes = self.__unsynch_get_script_history_objects_list(repo)[0]
                        who_changed = last_changes[JSON_ATTR_NAME__CHANGER]
                        when_changed = last_changes[JSON_ATTR_NAME__MODIFIED_DATE]

                        self._scripts_modification_info_by_id[script_id] = {
                            JSON_ATTR_NAME__CHANGER: who_changed,
                            JSON_ATTR_NAME__MODIFIED_DATE: when_changed,
                            JSON_ATTR_NAME__NAME: script_name,
                            JSON_ATTR_SCRIPT_ID: script_id
                        }

                        active_filename = script_file_name_with_ext
                        try:
                            conf_file_fp = open(merge_into_path([self._script_storage_path,
                                                                repo_candidate_dir,
                                                                REPO_CONF_FILENAME]), 'r')
                            configuration = ConfigParser.ConfigParser()
                            configuration.readfp(conf_file_fp)
                            active_filename = configuration.get(REPO_CONF_SECTION__SCRIPT_INFO,
                                                                REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP)
                            conf_file_fp.close()
                        except Exception:
                            pass

                        self._script_id_by_original_filename[active_filename] = script_id
                        script_file_in_storage_path = merge_into_path([self._script_storage_path, active_filename])
                        self._script_storage_file_path_by_id[script_id] = script_file_in_storage_path
                        shutil.copyfile(script_source_path, script_file_in_storage_path)
                        self._script_repo_file_path_by_id[script_id] = script_file_in_storage_path

                except Exception:
                    pass

        self._storage_daemon.start()

    @synchronized
    def get_scripts_in_storage_json(self):
        l = list(self._scripts_modification_info_by_id.values())
        l.sort()
        return json.dumps(l, indent=JSON_INDENT)

    @synchronized
    def update_script_in_storage(self, script_id, script_body, changer_username):
        if script_id not in self._repositories_by_script_id:
            raise NoSuchScriptInStorageException(script_id)

        repo = self._repositories_by_script_id[script_id]
        script_path = merge_into_path([self._script_storage_path,
                                       get_repo_dir_name_for_script_filename(script_id),
                                       script_id + ".json"])

        script_file = open(script_path, "w")
        script_file.write(script_body)
        script_file.close()
        shutil.copy(script_path, self._script_storage_file_path_by_id[script_id])

        update_script_in_repo(repo, script_id + ".json", "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER, changer_username))

    @synchronized
    def get_script_history_json(self, script_id):
        if script_id not in self._repositories_by_script_id:
            raise NoSuchScriptInStorageException(script_id)

        repo = self._repositories_by_script_id[script_id]
        r_list = self.__unsynch_get_script_history_objects_list(repo)

        return json.dumps(r_list, indent=JSON_INDENT)

    @synchronized
    def get_script(self, script_id):
        try:
            script_path = self._script_repo_file_path_by_id[script_id]
            script_file = open(script_path, "r")
            script = script_file.read().replace("\n", "")
            script_js = json.loads(script)
            script_file.close()

            return json.dumps(script_js, indent=JSON_INDENT)
        except Exception:
            raise NoSuchScriptInStorageException(script_id)

    @synchronized
    def get_script_revision(self, script_id, revision_hash):
        return self._unsynch_get_script_revision(script_id, revision_hash)

    @synchronized
    def fork_script_of_revision(self, script_id, revision_hash, creator_name, storage_filename):
        json_to_fork = self._unsynch_get_script_revision(script_id, revision_hash)
        res = self._unsynch_create_script_in_repo(creator_name, script_text=json_to_fork, st_filename=storage_filename)
        return res

    @synchronized
    def create_script_in_repo(self, creator_name, storage_filename):
        res = self._unsynch_create_script_in_repo(creator_name, st_filename=storage_filename)
        return res

    def __unsynch_get_script_history_objects_list(self, repo):
        hist_list = list_script_history(repo)
        r_list = []
        for hist_entity in hist_list:
            rev_hash = hist_entity[0]
            modification_date = hist_entity[1]
            hist_attributes = json.loads(hist_entity[2].replace("'", '"'))
            user_name = hist_attributes[REQUEST_PARAM_NAME__USER]

            r_list.append({JSON_ATTR_NAME__REVISION: rev_hash,
                           JSON_ATTR_NAME__MODIFIED_DATE: modification_date,
                           JSON_ATTR_NAME__CHANGER: user_name})
        return r_list

    def _unsynch_create_script_in_repo(self, creator_name, script_text=None, st_filename=None):
        script_id = self.unsynch_get_free_script_id()

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

        script_path = merge_into_path([self._script_storage_path,
                                       get_repo_dir_name_for_script_filename(script_id),
                                       script_id + ".json"])
        self._script_storage_file_path_by_id[script_id] = script_path
        repo = create_repo_for_script(self._script_storage_path, st_filename + '.json', script_id)

        new_script_obj = self._template_script_object
        if script_text is not None:
            new_script_obj = json.loads(script_text)

        new_script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__ID] = script_id
        script_name = new_script_obj[JSON_ATTR_NAME__PARAMS][JSON_ATTR_NAME__NAME]
        when_changed = datetime.datetime.fromtimestamp(time.time()).strftime(TIMESTAMP_FORMAT)

        self._scripts_modification_info_by_id[script_id] = {
            JSON_ATTR_NAME__CHANGER: creator_name,
            JSON_ATTR_NAME__MODIFIED_DATE: when_changed,
            JSON_ATTR_NAME__NAME: script_name,
            JSON_ATTR_SCRIPT_ID: script_id
        }
        self._script_id_by_original_filename[st_filename + '.json'] = script_id
        self._script_repo_file_path_by_id[script_id] = script_path

        write_script_object(script_path, new_script_obj)
        update_script_in_repo(repo, script_id + ".json", "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER, creator_name))
        self._repositories_by_script_id[script_id] = repo
        shutil.copy(script_path, merge_into_path([self._script_storage_path, st_filename + '.json']))

        return json.dumps(new_script_obj, indent=JSON_INDENT)

    def _unsynch_get_script_revision(self, script_id, revision_hash):
        if script_id not in self._repositories_by_script_id:
            raise NoSuchScriptInStorageException(script_id)

        repo = self._repositories_by_script_id[script_id]

        try:
            script_text = get_particular_script_version(repo, revision_hash, script_id + ".json")
        except BadObject:
            raise BadScriptRevisionException(revision_hash)

        script_json = json.loads(script_text)
        return json.dumps(script_json, indent=JSON_INDENT)

    def unsynch_get_free_script_id(self):
        script_id = self.__script_id_generator.next_id()

        while script_id in self._repositories_by_script_id:
            script_id = self.__script_id_generator.next_id()

        return script_id

    def get_lock(self):
        return self._storage_operations_lock

    def copy_to_storage(self, script_name, script_json):
        f = open(merge_into_path([self._script_storage_path, script_name]), 'w')
        f.write(script_json)
        f.close()


class ScriptUtils:
    __script_storage_manager = None
    __script_storage_path = None
    __script_storage_checking_period = STORAGE_DEFAULT_SCAN_PERIOD_MS
    __script_template_filename = None

    @staticmethod
    def set_scripts_storage_path(storage_path):
        ScriptUtils.__script_storage_path = storage_path

    @staticmethod
    def set_store_scan_period_in_ms(new_period):
        ScriptUtils.__script_storage_checking_period = new_period

    @staticmethod
    def initialize():
        if ScriptUtils.__script_storage_manager is None and (ScriptUtils.__script_storage_path is not None):
            print "initialize"
            ScriptUtils.__script_storage_manager = ScriptManager(ScriptUtils.__script_storage_path,
                                                                 ScriptUtils.__script_storage_checking_period,
                                                                 ScriptUtils.__script_template_filename)
    @staticmethod
    def set_script_template_filename(filename):
        ScriptUtils.__script_template_filename = filename

    @staticmethod
    def get_manager():
        man = ScriptUtils.__script_storage_manager
        if man is None:
            raise ScriptManagerNotInitializedException()
        assert isinstance(man, ScriptManager)
        return man