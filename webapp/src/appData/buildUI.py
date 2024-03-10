"""
"""

import glob
import json
import os
import sys

import pystache

_, dir_in, js_out = sys.argv

file_data = {}
pystache_renderer = pystache.Renderer(escape=lambda x: x, missing_tags="strict")


def read_file(path, allow_missing=True):
    path = os.path.realpath(path)
    if path not in file_data:
        if not os.path.exists(path):
            if not allow_missing:
                raise FileNotFoundError(path)
            data = None
        else:
            print(path)
            with open(path, encoding="utf-8") as file:
                data = file.read().strip()
        file_data[path] = data
    return file_data[path]


def _render(context: dict) -> str:
    items = ["%s:%s" % x for x in context.items()]
    result = "{" + ",".join(items) + "}"
    return result


def _sort_data(contexts: list) -> list:
    return contexts


def load_data():
    data = []
    # find input json files and load
    for path in glob.glob(dir_in + "/**/*.json", recursive=True):
        print(path)
        id, _ = os.path.splitext(os.path.basename(path))
        with open(path, encoding="utf-8") as file:
            context = json.load(file)
        # context["id"] = id
        context["$path"] = path
        data.append(context)
    return data


def sort_data(data):
    # group and sort data

    data_by_id = {}
    for d in data:
        data_by_id[d["id"]] = d
        d["$children"] = []

    for d in data:
        pid = d["parentId"]
        if pid not in data_by_id:
            print(f"warning: added external node id: {pid}")
            data_by_id[pid] = {"id": pid, "external": True, "$children": []}
        data_by_id[pid]["$children"].append(d["id"])

    # sort children by id
    for d in data:
        d["$children"] = sorted(d["$children"])

    def iter_tree(ids):
        """parents first"""
        for id in ids:
            yield id
            yield from iter_tree(data_by_id[id]["$children"])

    external_ids = sorted(d["id"] for d in data_by_id.values() if d.get("external"))
    ids_sorted = list(iter_tree(external_ids))
    data = [data_by_id[id] for id in ids_sorted if id not in external_ids]

    return data


data = load_data()
data = sort_data(data)

results = []
for context in data:
    result = {}
    result["id"] = json.dumps(context["id"])
    result["parentId"] = json.dumps(context["parentId"])
    if "name" in context:
        result["name"] = json.dumps(context["name"])

    # schema location => template data
    schema = context["$schema"]
    path = context["$path"]
    basedir = os.path.dirname(path)
    schema_path = basedir + "/" + schema
    comp_path = os.path.dirname(os.path.abspath(schema_path))

    html = read_file(comp_path + "/html.html")
    if html:
        result["html"] = json.dumps(pystache_renderer.render(html, context))

    set_value = read_file(comp_path + "/setValue.js")
    if set_value:
        result["setValue"] = pystache_renderer.render(set_value, context)

    get_value = read_file(comp_path + "/getValue.js")
    if get_value:
        result["getValue"] = pystache_renderer.render(get_value, context)

    results.append(result)

# for context in sort_data(contexts):
#    result = render(context)
#    data.append(result)

# serialize data

results = [[f"{k}: {v}" for k, v in x.items()] for x in results]
results = ["{\n" + ",\n".join(x) + "\n}" for x in results]
results = ",\n".join(results)

text_js = "export default [" + results + "];"
with open(js_out, "w", encoding="utf-8") as file:
    file.write(text_js)
