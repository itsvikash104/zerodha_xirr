import json


def read_json_file(file):
    with open(file, "r") as read_file:
        data = json.load(read_file)
    return data


def write_json_file(obj, file):
    with open(file, "w") as write_file:
        json.dump(obj, file)


def read_file_as_string(file):
    with open(file, "r") as read_file:
        data = read_file.read()
    return data


def get_cookie(file_path):
    with open(file_path, "r") as cookie_file:
        cookie_string = cookie_file.read()
    cookies = {}
    for cookie in cookie_string.split(";"):
        key, value = cookie.split("=")
        cookies[key] = value
    return cookies
