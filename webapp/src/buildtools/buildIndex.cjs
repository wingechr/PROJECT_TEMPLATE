"use strict";

const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const utils = require("./buildUtils.cjs");

const [_node, script, uiJs, inHtml, outHtml] = process.argv;
const scriptDir = path.dirname(path.resolve(script));

const uiJsRel = utils.getRelPath(scriptDir, uiJs);

let html = fs.readFileSync(inHtml, "utf8");

import(uiJsRel).then((mod) => {
  const dom = new JSDOM(html);
  for (const exp of mod.default) {
    exp.component.createStatic(dom.window.document);
  }

  html = dom.serialize();
  fs.writeFileSync(outHtml, html, "utf8");
});
