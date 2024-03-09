"use strict";
// node src/appData/buildFunctions.cjs src/appData/functions src/appData/build/functions.js

const fs = require("fs");
const path = require("path");
const glob = require("glob");
const acorn = require("acorn");

const [_node, _script, funDir, jsOut] = process.argv;
const jsOutDir = path.dirname(path.resolve(jsOut)); // absolute path

/**
 *
 * @param {string} directory
 * @returns {Promise} resolves to list of paths
 */
function findJSFiles(directory) {
  return glob.glob(directory + "/**/*.js");
}

/**
 *
 * @param {str} filePath
 * @returns {array} of {filepath, name, params, isDefault}
 */
function extractFunctions(filePath) {
  const filepathRel = path
    .relative(jsOutDir, path.resolve(filePath))
    .replace(/\\/g, "/");
  const code = fs.readFileSync(filePath, "utf-8");
  const ast = acorn.parse(code, { sourceType: "module", ecmaVersion: 2000 });
  const fun2params = {};
  const result = [];
  ast.body.forEach((node) => {
    if (node.type === "ExportDefaultDeclaration") {
      // exported default function
      node = node.declaration;
      result.push({
        filepathRel,
        name: node.id.name,
        params: node.params.map((x) => x.name),
        isDefault: true,
      });
    }

    if (node.type === "FunctionDeclaration") {
      // save function params
      const name = node.id.name;
      const params = node.params.map((x) => x.name);
      fun2params[name] = params;
    } else if (node.type === "ExportNamedDeclaration") {
      // multiple exports (with alias)
      for (const spec of node.specifiers) {
        result.push({
          filepathRel,
          name: spec.exported.name,
          params: fun2params[spec.local.name],
          isDefault: false,
        });
      }
    }
  });
  return result;
}

/**
 * order functions so that dependencies are not violated
 * @param {array} functions: array of {filepath, name, params, isDefault}
 * @returns array of {filepath, name, params, isDefault}
 */
function sortFunctions(functions) {
  const todo = functions.slice(); // must still be be sorted (start with flat copy)
  const done = []; // already sorted
  /**
   * we do this in a very simple way:
   * check the first function of the queue:
   *   if any params refer to functions that are still in the TODO list:
   *   defer for later (end of queue).
   *   otherwise: remove from queue
   *
   */

  while (todo.length > 0) {
    const fun = todo.shift(); // dequeue first element
    let defer = false;
    for (const p of fun.params) {
      if (todo.map((f) => f.name).indexOf(p) > -1) {
        defer = true;
        break;
      }
    }
    if (defer) {
      todo.push(fun);
    } else {
      done.push(fun);
    }
  }
  return done;
}

findJSFiles(path.resolve(funDir)).then((files) => {
  let functions = []; // array of {filepath, name, params, isDefault}
  for (const file of files) {
    let functionsFile = extractFunctions(file);
    console.log(file, functionsFile.length);
    functions = functions.concat(functionsFile);
  }
  functions = sortFunctions(functions);
  // create code

  let imports = [];
  let exports = [];
  for (const fun of functions) {
    let imp = fun.name;
    if (fun.isDefault) {
      imp = "default as " + imp;
    }
    imports.push(`import {${imp}} from "${fun.filepathRel}";`);

    exports.push(
      `{ name: "${fun.name}", dependencies: ${JSON.stringify(fun.params)}, callable: ${fun.name} }`,
    );
  }
  const text =
    imports.join("\n") + "\nexport default [\n" + exports.join(",\n") + "\n];";

  fs.writeFileSync(jsOut, text);
});
