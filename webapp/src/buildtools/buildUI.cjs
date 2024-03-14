"use strict";

const fs = require("fs");
const path = require("path");
const utils = require("./buildUtils.cjs");

function sortExports(exports, externalIds) {
  /* initialize nodes in tree */
  externalIds = externalIds || [];
  const tree = {};
  const byId = {};
  for (const exp of exports) {
    const obj = exp.object;
    const id = obj.id;
    const parentId = obj.parentId;
    if (tree[id]) {
      throw new Error(`duplicate id ${id}`);
    }
    tree[id] = [];
    byId[id] = exp;
  }

  /* link nodes, find externals */
  for (const exp of exports) {
    const obj = exp.object;
    const id = obj.id;
    const parentId = obj.parentId;
    if (!tree[parentId]) {
      if (externalIds.indexOf(parentId) == -1) {
        throw new Error(
          `Not defined external id: ${parentId} not in ${externalIds}`,
        );
      }
      tree[parentId] = [];
    }
    tree[parentId].push(id);
  }

  // walk through tree and create
  // sorted array of ids in orderedIds
  const orderedIds = [];
  function walk(ids) {
    // sort
    ids.sort();
    for (const id of ids) {
      // save id (except externals)
      if (externalIds.indexOf(id) == -1) {
        orderedIds.push(id);
      }
      // recursion
      walk(tree[id]);
    }
  }

  walk(externalIds);

  // return objects
  const result = orderedIds.map((id) => byId[id]);

  return result;
}

function save(items, filepath) {
  let imports = [];
  let exports = [];
  for (const i in items) {
    const it = items[i];
    const filepathRel = it.relPath;
    const basename = path
      .basename(filepathRel)
      .replace(".js", "")
      .replace("-", "_");
    const nameImp = it.name;
    const name = `comp_${i}_${basename}_${nameImp}`;
    const id = it.object.id;
    const parentId = it.object.parentId;
    imports.push(`import {${nameImp} as ${name}} from "${filepathRel}";`);
    exports.push(
      `{ id: "${id}", parentId: "${parentId}", component: ${name} }`,
    );
  }
  const text =
    imports.join("\n") + "\nexport default [\n" + exports.join(",\n") + "\n];";

  fs.writeFileSync(filepath, text);
}

const [_node, script, indexHtmlPath, inputDir, jsOut] = process.argv;
const scriptDir = path.dirname(path.resolve(script));
const outDir = path.dirname(path.resolve(jsOut));
const externalDIvIds = utils.extractDivIds(indexHtmlPath);

utils
  .findJSFiles(inputDir)
  .then((x) => x.sort())
  .then((x) => utils.loadFiles(x, scriptDir))
  .then((x) => utils.getExports(x, outDir))
  .then((x) => sortExports(x, externalDIvIds))
  .then((exps) => save(exps, jsOut));
