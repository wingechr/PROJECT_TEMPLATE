"use strict";

// require("@babel/polyfill"); // old browser compatibility
// const $ = require("jquery"); // defined externally
// const _ = require("lodash"); // imported

const examplePlusOne = require("./lib/mylib.js").examplePlusOne;

// expose to main library
module.exports = {
  examplePlusOne: examplePlusOne,
};
