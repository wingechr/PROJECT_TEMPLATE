"use strict";

const fs = require("fs");
const path = require("path");
const utils = require("./buildUtils.cjs");

function getFunctionInfo(func) {
  // Get the name of the function
  const name = func.name;

  // Get the source code of the function
  const functionSource = func.toString();

  // Use regular expressions to parse parameter names
  const parameterNames =
    functionSource
      .slice(functionSource.indexOf("(") + 1, functionSource.indexOf(")"))
      .match(/([^\s,]+)/g) || [];

  return [name, parameterNames];
}

function sortExports(exports, data) {
  let dataIds = new Set(Object.keys(data));
  let todo = exports;
  let done = [];
  let maxDefer = todo.length; // no infinite iterations

  // find function dependencies
  for (const exp of exports) {
    const [nameDef, dependencies] = getFunctionInfo(exp.object);
    exp.dependencies = dependencies;
    exp.nameDef = nameDef;
    exp.id = exp.name == "default" ? exp.nameDef : exp.name;
  }

  while (todo.length > 0) {
    const exp = todo.shift(); // pop first element
    /* if all dependencies are in dataIds: push on results,
    otherwiese: put at end andcheck later
    */

    let isOk = true;
    for (const d of exp.dependencies) {
      if (!dataIds.has(d)) {
        isOk = false;
        break;
      }
    }

    if (isOk) {
      done.push(exp);
      //console.log(`adding ${exp.id}`);
      maxDefer = todo.length;
      dataIds.add(exp.id);
    } else {
      //console.log(`deferring ${exp.id}`);
      todo.push(exp);
    }

    // prevent infinite loop in dependency cycles
    if (maxDefer < 0) {
      throw new Error(
        `Infinite loop: Dependency cycle: ${JSON.stringify(todo)}`,
      );
    } else {
      maxDefer -= 1;
    }
  }
  return done;
}

function save(items, filepath) {
  let imports = [];
  let exports = [];
  for (const it of items) {
    imports.push(`import {${it.name} as ${it.id}} from "${it.relPath}";`);
    const deps = JSON.stringify(it.dependencies);
    exports.push(
      `{ name: "${it.id}", dependencies: ${deps}, callable: ${it.id} }`,
    );
  }
  const text =
    imports.join("\n") + "\nexport default [\n" + exports.join(",\n") + "\n];";

  fs.writeFileSync(filepath, text);
}

const [_node, script, dataJsonPath, inputDir, jsOut] = process.argv;
const scriptDir = path.dirname(path.resolve(script));
const outDir = path.dirname(path.resolve(jsOut));
const reldataJsonPath = utils.getRelPath(scriptDir, dataJsonPath);
const data = require(reldataJsonPath);

utils
  .findJSFiles(inputDir)
  .then((x) => x.sort())
  .then((x) => utils.loadFiles(x, scriptDir))
  .then((x) => utils.getExports(x, outDir))
  .then((x) => sortExports(x, data))
  .then((exps) => save(exps, jsOut));
