import os
import re
import git

from datetime import datetime
from wibses.utils import merge_into_path, get_repo_name_for_script


def create_repo_for_script(scripts_store_path, script_name):
    script_dir = merge_into_path([scripts_store_path, get_repo_name_for_script(script_name)])
    if not os.path.exists(script_dir):
        os.mkdir(script_dir)
    return git.Repo.init(script_dir)


def get_repo_for_script(scripts_store_path, script_name):
    script_dir = merge_into_path([scripts_store_path, get_repo_name_for_script(script_name)])
    return git.Repo(script_dir)


def update_script_in_repo(repository, script_full_name, update_info_string):
    repository.git.add(script_full_name)
    repository.git.commit(m=update_info_string)


def list_script_history(repository):
    result_list = []
    for commit in repository.iter_commits():
        commit_timestamp = datetime.fromtimestamp(commit.committed_date)
        commit_date_str = commit_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        update_info_string_raw = commit.message
        update_info_string = re.search(r'\{.*\}', update_info_string_raw).group(0)
        revision_hash = commit.name_rev.split()[0]

        result_list.append((revision_hash, commit_date_str, update_info_string))
    return result_list


def get_particular_script_version(repository, revision_hash, script_name):
    commit = repository.commit(revision_hash)
    return commit.tree[script_name].data_stream.read().replace("\n", "")


def reset_to_particular_script_version(repository, revision_hash):
    repository.head.reset(revision_hash)