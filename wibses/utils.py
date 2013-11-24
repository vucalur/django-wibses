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


def jsonp(f):
    """
    Wrap a json response in a callback, and set the mimetype (Content-Type) header accordingly
    (will wrap in text/javascript if there is a callback). If the "callback" or "jsonp" paramters
    are provided, will wrap the json output in callback({thejson})

    Usage:

    @jsonp
    def my_json_view(request):
        d = { 'key': 'value' }
        return HTTPResponse(json.dumps(d), content_type='application/json')


    Based on: https://gist.github.com/sivy/871954
    """
    from functools import wraps

    @wraps(f)
    def jsonp_wrapper(request, *args, **kwargs):
        resp = f(request, *args, **kwargs)
        if resp.status_code != 200:
            return resp

        callback = None
        if 'callback' in request.GET:
            callback = request.GET['callback']
        elif 'jsonp' in request.GET:
            callback = request.GET['jsonp']
        else:
            return resp

        resp['Content-Type'] = 'application/javascript; charset=utf-8'
        resp.content = "%s(%s);" % (callback, resp.content)
        return resp

    return jsonp_wrapper