import os


def get_folder_containing_names(path, incl_file_names=False, incl_dir_names=False):
    if not (incl_dir_names or incl_file_names):
        return None

    from os import walk

    for dir_name, dir_names, file_names in walk(path):
        if incl_file_names and incl_dir_names:
            return dir_names, file_names
        elif incl_dir_names:
            return dir_names
        elif incl_file_names:
            return file_names


def merge_into_path(files_paths_list):
    result_path = files_paths_list[0]
    if len(files_paths_list) > 1:
        for path in files_paths_list[1:]:
            result_path += os.sep + path

    while True:
        old_len = len(result_path)
        result_path = result_path.replace(os.sep*2, os.sep)
        if old_len == len(result_path):
            break

    return result_path


def get_repo_name_for_script(script_name):
    return "." + script_name


def get_script_name_from_repo(repo_dir_name):
    return repo_dir_name[1:]


def create_template_script_json():
    tmp_script_text = """
    {
    "sections": [
        {
            "params": {
                "threshold": 112
            },
            "sentences": [
                {
                    "params": {
                        "obligatory": false,
                        "threshold": 15,
                        "name": "Sample Sentence"
                    },
                    "slots": [
                        {
                            "params": {
                                "obligatory": false,
                                "threshold": 60,
                                "name": "Sample slot"
                            },
                            "tokens": []
                        }
                    ]
                }
            ],
            "type": "synthetic"
        },
        {
            "params": {
                "threshold": 50
            },
            "sentences": [
                {
                    "params": {
                        "obligatory": false,
                        "threshold": 55,
                        "name": "Sample Sentence 2"
                    },
                    "slots": [
                        {
                            "params": {
                                "obligatory": false,
                                "threshold": 60,
                                "name": "Sample slot"
                            },
                            "tokens": []
                        }
                    ]
                }
            ],
            "type": "analytical"
        },
        {
            "params": {
                "threshold": 50
            },
            "sentences": [
                {
                    "params": {
                        "obligatory": false,
                        "threshold": 55,
                        "name": "Sample Sentence 1"
                    },
                    "slots": [
                        {
                            "params": {
                                "obligatory": false,
                                "threshold": 60,
                                "name": "Sample slot"
                            },
                            "tokens": []
                        }
                    ]
                }
            ],
            "type": "circumstances"
        }
    ],
    "params": {
        "name": "Some Semantic script"
    }
}

    """
    return tmp_script_text