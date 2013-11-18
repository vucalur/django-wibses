import atexit
import json
from multiprocessing.synchronize import Lock
import shutil
import threading
from gitdb.exc import BadObject
import time
import re

from wibses import ENV_SCRIPT_STORAGE_PATH_NAME
from wibses.data_store import JSON_INDENT, REQUEST_PARAM_NAME__USER, JSON_ATTR_NAME__REVISION, \
    JSON_ATTR_NAME__MODIFIED_DATE, JSON_ATTR_NAME__CHANGER, STORAGE_DEFAULT_SCAN_PERIOD_MS, \
    DEFAULT_STORAGE_SCRIPT_CREATOR_NAME
from wibses.data_store.exceptions import NoSuchScriptInStorageException, BadScriptRevisionException, \
    ScriptAlreadyExistsInStorageException
from wibses.data_store.repo_management import get_repo_for_script, list_script_history, \
    get_particular_script_version, create_repo_for_script, update_script_in_repo
from wibses.utils import get_folder_containing_names, merge_into_path, get_script_name_from_repo, \
    get_repo_name_for_script, create_template_script_json


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
        self._sleep_per_in_seconds = checking_period_ms / 1000.0
        assert isinstance(script_manager, ScriptManager)
        self._script_manager = script_manager
        self._stop = False
        threading.Thread.__init__(self)

    def get_lock(self):
        return self._script_manager.get_lock()

    def stop_me(self):
        self._stop = True

    def run(self):
        while not self._stop:
            self.do_work()
            time.sleep(self._sleep_per_in_seconds)

    @synchronized
    def do_work(self):
        file_names = get_folder_containing_names(self._script_manager._script_storage_path, incl_file_names=True)
        patt = r'(.+)\.json'
        script_names_without_ext = map(lambda x: re.search(patt, x).group(1),
                                       filter(lambda x: re.search(patt, x) is not None,
                                              file_names))
        manager_scripts = self._script_manager._scripts_repositories
        for script_name in script_names_without_ext:
            if script_name not in manager_scripts:
                script_path = merge_into_path([self._script_manager._script_storage_path,
                                               get_repo_name_for_script(script_name),
                                               script_name + ".json"])
                repo = create_repo_for_script(self._script_manager._script_storage_path, script_name)

                shutil.copyfile(merge_into_path([self._script_manager._script_storage_path, script_name + ".json"]),
                                script_path)

                update_script_in_repo(repo,
                                      script_name + ".json", "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER,
                                                                              DEFAULT_STORAGE_SCRIPT_CREATOR_NAME))
                self._script_manager._scripts_repositories[script_name] = repo


class ScriptManager:
    def __init__(self, script_storage_path, storage_checker_period):
        self._script_storage_path = script_storage_path
        self._scripts_repositories = {}
        self._storage_operations_lock = Lock()
        self._storage_daemon = StorageDaemon(storage_checker_period, self)

        inner_dirs = get_folder_containing_names(script_storage_path, incl_dir_names=True)
        for candidate in inner_dirs:
            candidate_path = merge_into_path([script_storage_path, candidate])
            candidate_inner_dirs, candidate_inner_files = get_folder_containing_names(candidate_path,
                                                                                      incl_dir_names=True,
                                                                                      incl_file_names=True)
            if ".git" in candidate_inner_dirs:
                script_name = get_script_name_from_repo(candidate)
                self._scripts_repositories[script_name] = get_repo_for_script(script_storage_path, script_name)
                script_name_with_ext = script_name + ".json"
                shutil.copyfile(merge_into_path([self._script_storage_path, candidate, script_name_with_ext]),
                                merge_into_path([self._script_storage_path, script_name_with_ext]))
        self._storage_daemon.start()

    def stop_storage_daemon(self):
        self._storage_daemon.stop_me()
        self._storage_daemon.join()

    def get_lock(self):
        return self._storage_operations_lock

    def copy_to_storage(self, script_name, script_json):
        f = open(merge_into_path([self._script_storage_path, script_name]), 'w')
        f.write(script_json)
        f.close()

    @synchronized
    def get_scripts_in_storage_json(self):
        l = list(self._scripts_repositories.keys())
        l.sort()
        return json.dumps(l, indent=JSON_INDENT)

    @synchronized
    def update_script_in_storage(self, script_name, script_body, changer_username):
        if script_name not in self._scripts_repositories:
            raise NoSuchScriptInStorageException(script_name)

        repo = self._scripts_repositories[script_name]
        script_path = merge_into_path([self._script_storage_path,
                                       get_repo_name_for_script(script_name),
                                       script_name + ".json"])

        script_file = open(script_path, "w")
        script_file.write(script_body)
        script_file.close()
        self.copy_to_storage(script_name+".json", script_body)

        update_script_in_repo(repo, script_name + ".json", "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER, changer_username))

    @synchronized
    def get_script_history_json(self, script_name):
        if script_name not in self._scripts_repositories:
            raise NoSuchScriptInStorageException(script_name)

        repo = self._scripts_repositories[script_name]
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

        return json.dumps(r_list, indent=JSON_INDENT)

    @synchronized
    def get_script(self, script_name):
        script_path = merge_into_path([self._script_storage_path,
                                       get_repo_name_for_script(script_name),
                                       script_name + ".json"])
        try:
            script_file = open(script_path, "r")
            script = script_file.read().replace("\n", "")
            script_js = json.loads(script)
            script_file.close()

            return json.dumps(script_js, indent=JSON_INDENT)
        except IOError:
            raise NoSuchScriptInStorageException(script_name)

    @synchronized
    def get_script_revision(self, script_name, revision_hash):
        return self._unsynch_get_script_revision(script_name, revision_hash)

    def _unsynch_get_script_revision(self, script_name, revision_hash):
        if script_name not in self._scripts_repositories:
            raise NoSuchScriptInStorageException(script_name)

        repo = self._scripts_repositories[script_name]

        try:
            script_text = get_particular_script_version(repo, revision_hash, script_name + ".json")
        except BadObject:
            raise BadScriptRevisionException(revision_hash)

        script_json = json.loads(script_text)

        return json.dumps(script_json, indent=JSON_INDENT)

    @synchronized
    def fork_script_of_revision(self, script_name, revision_hash, new_script_name, creator_name):
        json_to_fork = self._unsynch_get_script_revision(script_name, revision_hash)

        new_storage_script_path = merge_into_path([self._script_storage_path, new_script_name + ".json"])
        new_file = open(new_storage_script_path, "w")
        new_file.write(json_to_fork)
        new_file.close()

        repo = create_repo_for_script(self._script_storage_path, new_script_name)
        self._scripts_repositories[new_script_name] = repo

        script_repo_path = merge_into_path([self._script_storage_path,
                                           get_repo_name_for_script(new_script_name),
                                           new_script_name + ".json"])

        shutil.copyfile(new_storage_script_path, script_repo_path)
        update_script_in_repo(repo, new_script_name + ".json", "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER, creator_name))

        return json.dumps(json.loads(json_to_fork), indent=JSON_INDENT)

    @synchronized
    def create_script_in_repo(self, script_name, creator_name):
        if script_name in self._scripts_repositories:
            raise ScriptAlreadyExistsInStorageException(script_name)

        template_script_text = create_template_script_json()
        script_path = merge_into_path([self._script_storage_path,
                                       get_repo_name_for_script(script_name),
                                       script_name + ".json"])
        repo = create_repo_for_script(self._script_storage_path, script_name)

        script_file = open(script_path, "w")
        script_file.writelines([template_script_text])
        script_file.close()

        self.copy_to_storage(script_name + '.json', template_script_text)

        update_script_in_repo(repo, script_name + ".json", "{'%s':'%s'}" % (REQUEST_PARAM_NAME__USER, creator_name))
        self._scripts_repositories[script_name] = repo

        return json.dumps(json.loads(template_script_text), indent=JSON_INDENT)


class ScriptUtils:
    __script_storage_manager = None
    __script_storage_path = None
    __script_storage_checking_period = STORAGE_DEFAULT_SCAN_PERIOD_MS

    @staticmethod
    def setup_storage_daemon_shutdown_hook(script_manager):
        def st_daemon_shutdown_hook():
            script_manager.stop_storage_daemon()
        atexit.register(st_daemon_shutdown_hook)

    @staticmethod
    def set_dictionary_storage_path(storage_path):
        ScriptUtils.__script_storage_path = storage_path

    @staticmethod
    def set_store_scan_period_in_ms(new_period):
        ScriptUtils.__script_storage_checking_period = new_period

    @staticmethod
    def initialize_from_environment():
        import os

        environ = os.environ

        if ENV_SCRIPT_STORAGE_PATH_NAME in environ:
            script_storage_dir = environ[ENV_SCRIPT_STORAGE_PATH_NAME]
            ScriptUtils.__script_storage_manager = ScriptManager(script_storage_dir,
                                                                 ScriptUtils.__script_storage_checking_period)
            ScriptUtils.setup_storage_daemon_shutdown_hook(ScriptUtils.__script_storage_manager)

    @staticmethod
    def initialize_from_current_config():
        if ScriptUtils.__script_storage_path is not None:
            ScriptUtils.__script_storage_manager = ScriptManager(ScriptUtils.__script_storage_path,
                                                                 ScriptUtils.__script_storage_checking_period)
            ScriptUtils.setup_storage_daemon_shutdown_hook(ScriptUtils.__script_storage_manager)

    @staticmethod
    def get_manager():
        man = ScriptUtils.__script_storage_manager
        if man is None:
            raise ScriptManagerNotInitializedException()
        assert isinstance(man, ScriptManager)
        return man