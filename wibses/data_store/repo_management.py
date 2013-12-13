import os
import re
from datetime import datetime

import git

from . import TIMESTAMP_FORMAT, REPO_GITIGNORE_FILENAME, REPO_IGNORED_FILENAMES, \
    REPO_CONF_SECTION__SCRIPT_INFO, REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP, REPO_CONF_FILENAME
from ..utils import merge_into_path, get_repo_dir_name_for_script_filename


def create_repo_for_script(scripts_store_path, script_filename_with_ext, script_id):
    script_dir = merge_into_path([scripts_store_path, get_repo_dir_name_for_script_filename(script_id)])
    if not os.path.exists(script_dir):
        os.mkdir(script_dir)
    # create gitignore file
    gitignore_fp = open(merge_into_path([script_dir, REPO_GITIGNORE_FILENAME]), 'w')
    for l in REPO_IGNORED_FILENAMES:
        gitignore_fp.write(l + '\n')
    gitignore_fp.close()
    #create repoinfo file
    repo_cfg_file_text = "[%s]\n%s = %s\n" % (REPO_CONF_SECTION__SCRIPT_INFO,
                                              REPO_CONF_ORIGINAL_SCRIPT_FILENAME_PROP,
                                              script_filename_with_ext)
    repo_cfg_file_fp = open(merge_into_path([script_dir, REPO_CONF_FILENAME]), "w")
    repo_cfg_file_fp.write(repo_cfg_file_text)
    repo_cfg_file_fp.close()

    return git.Repo.init(script_dir)


def get_repo_for_script(scripts_store_path, script_name, repo_name=None):
    if repo_name is None:
        repo_name = get_repo_dir_name_for_script_filename(script_name)
    script_dir = merge_into_path([scripts_store_path, repo_name])
    return git.Repo(script_dir)


def update_script_in_repo(repository, script_full_name, update_info_string):
    repository.git.add(script_full_name)
    repository.git.commit(m=update_info_string)


def list_script_history(repository):
    result_list = []
    for commit in repository.iter_commits():
        commit_timestamp = datetime.fromtimestamp(commit.committed_date)
        commit_date_str = commit_timestamp.strftime(TIMESTAMP_FORMAT)

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