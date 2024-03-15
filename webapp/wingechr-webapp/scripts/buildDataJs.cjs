"use strict";

const fs = require("fs");
const [_node, script, inJson, outJs] = process.argv;

let text = fs.readFileSync(inJson, "utf8");
text = "export default " + text + ";";
fs.writeFileSync(outJs, text, "utf8");
