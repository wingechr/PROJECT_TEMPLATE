"use strict";

const path = require("path");
const glob = require("glob");
const fs = require("fs");
const { JSDOM } = require("jsdom");

/**
 *
 * @param {string} directory
 * @returns {Promise} resolves to list of paths
 */
function findMJSFiles(directory) {
  const filePaths = glob.glob(directory + "/**/*.mjs");
  return filePaths;
}

function getRelPath(dirFrom, filePath) {
  return (
    "./" + path.relative(dirFrom, path.resolve(filePath)).replace(/\\/g, "/")
  );
}

function loadFiles(filePaths) {
  return Promise.all(
    filePaths.map((fp) => {
      let fpRel = getRelPath(__dirname, fp);
      console.log(fpRel);
      return import(fpRel).then((mod) => [fp, mod]);
    }),
  );
}

function getExports(files_modules, outDir) {
  const exports = [];
  for (const [fp, mod] of files_modules) {
    for (const [name, obj] of Object.entries(mod)) {
      const fpRel = getRelPath(outDir, fp);
      exports.push({ relPath: fpRel, name: name, object: obj });
    }
  }
  return exports;
}

function extractDivIds(filepathHtml) {
  // Read the HTML file
  const html = fs.readFileSync(filepathHtml, "utf8");
  const dom = new JSDOM(html);
  // Extract div ids
  const divIds = [];
  dom.window.document.querySelectorAll("*").forEach((e) => {
    const id = e.id.trim();
    if (id) {
      divIds.push(id);
    }
  });

  return divIds;
}

module.exports = {
  getExports,
  findJSFiles: findMJSFiles,
  loadFiles,
  getRelPath,
  extractDivIds,
};
