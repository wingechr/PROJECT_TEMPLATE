"""
python src/appData/buildData.py src/appData/data src/appData/build/data.js
"""

import glob
import json
import os
import re
import sys

import openpyxl

PATTERN_EXCEL = r"^=\[([^]]+)\]([^!]+)\!(.+)$"


def resolve_excel(data_from_excel: dict):
    for file, specs in data_from_excel.items():
        wb = openpyxl.load_workbook(file, read_only=True, data_only=True)
        for spec in specs:
            sht = wb[spec["sheet"]]
            val = sht[spec["range"]].value
            assert isinstance(val, (int, float))
            yield spec["key"], val


_, dir_in, json_out = sys.argv

data = {}
data_from_excel = {}


def add_dict_unique(dct, key, val):
    assert key not in dct, key
    dct[key] = val


for path in glob.glob(dir_in + "/**/*.json", recursive=True):
    # skip output
    if os.path.abspath(json_out) == os.path.abspath(path):
        continue

    basedir = os.path.dirname(path)
    print(path)
    with open(path, encoding="utf-8") as file:
        specs = json.load(file)

    for key, val in specs.items():
        if isinstance(val, str) and re.match(PATTERN_EXCEL, val):
            path, sheet, range = re.match(PATTERN_EXCEL, val).groups()
            path = basedir + "/" + path
            if path not in data_from_excel:
                data_from_excel[path] = []
            data_from_excel[path].append({"key": key, "sheet": sheet, "range": range})
        else:
            add_dict_unique(data, key, val)
for key, val in resolve_excel(data_from_excel):
    add_dict_unique(data, key, val)


text = json.dumps(data, indent=2, ensure_ascii=False)

with open(json_out, "w", encoding="utf-8") as file:
    file.write(text)

# with open(js_out, "w", encoding="utf-8") as file:
#    file.write(f"export default {text};")
