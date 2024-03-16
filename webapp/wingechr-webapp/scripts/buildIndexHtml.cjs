"use strict";

const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const utils = require("./utils/index.cjs");

const [_node, script, uiJs, inHtml, outHtml, createStaticHtml] = process.argv;
const scriptDir = path.dirname(path.resolve(script));

const uiJsRel = utils.getRelPath(scriptDir, uiJs);

let html = fs.readFileSync(inHtml, "utf8");

import(uiJsRel).then((mod) => {
  const dom = new JSDOM(html);
  if (createStaticHtml.toLowerCase() == "true") {
    for (const component of mod.default) {
      component.createHtml(dom.window.document);
    }
  }

  html = dom.serialize();
  fs.writeFileSync(outHtml, html, "utf8");
});
