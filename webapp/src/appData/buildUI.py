"""
"""

import glob
import json
import os
import re
import sys

_, dir_in, js_out = sys.argv

file_data = {}


def read_file(path, allow_missing=True):
    path = os.path.realpath(path)
    if path not in file_data:
        if not os.path.exists(path):
            if not allow_missing:
                raise FileNotFoundError(path)
            data = None
        else:
            with open(path, encoding="utf-8") as file:
                data = file.read().strip()
        file_data[path] = data
    return file_data[path]


def render(context: dict) -> str:
    items = ["%s:%s" % x for x in context.items()]
    result = "{" + ",".join(items) + "}"
    return result


def sort_data(contexts: list) -> list:
    return contexts


data = []
# find input files
for path in glob.glob(dir_in + "/**/*.json", recursive=True):
    print(path)
    basedir = os.path.dirname(path)
    id, _ = os.path.splitext(os.path.basename(path))
    with open(path, encoding="utf-8") as file:
        context = json.load(file)

    context["id"] = id
    schema = context.pop("$schema")

    for k, v in context.items():
        context[k] = json.dumps(v)

    # find schema file
    schema_path = basedir + "/" + schema
    comp_path = os.path.dirname(os.path.abspath(schema_path))

    ui_html = read_file(comp_path + "/ui.html")
    if ui_html:
        context["html"] = json.dumps(ui_html)

    get_value_js = read_file(comp_path + "/getValue.js")
    if get_value_js:
        context["getValue"] = re.sub("^export ", "", get_value_js)

    set_value_js = read_file(comp_path + "/setValue.js")
    if set_value_js:
        context["setValue"] = re.sub("^export ", "", set_value_js)

    context = render(context)
    data.append(context)


# for context in sort_data(contexts):
#    result = render(context)
#    data.append(result)

with open(js_out, "w", encoding="utf-8") as file:
    text = "export default [" + ",\n".join(data) + "];"
    file.write(text)
