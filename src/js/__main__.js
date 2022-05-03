"use strict";

// const $ = require("jquery"); // defined externally
// const _ = require("lodash"); // imported

const plusOne = require("./lib/mylib.js").plusOne;

// expose to main library
module.exports = {
  plusOne: plusOne,
};
