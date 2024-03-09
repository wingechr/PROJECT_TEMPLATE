"use strict";
import _ from "lodash";

const IS_DEBUG = process.env.NODE_ENV == "development";
/* only use console.log in development */
let console_log;
if (IS_DEBUG) {
  console_log = function (msg) {
    /*
    if (typeof msg != "string") {
      msg = JSON.stringify(msg);
    }
    */
    console.log(msg);
  };
} else {
  // dummy function
  console_log = function (msg) {};
}

/**
 * we could also do a lodash deep equal, but I don't thinks it's worth the trouble.
 * it's good enough that it works on primitive data
 * @param {*} x
 * @param {*} y
 * @returns {boolean}
 */
function isDifferent(x, y) {
  /*
   */
  return !_.isEqual(x, y);
}

/**
 * @param {object} defaultData
 * @returns {object}
 */
function getInitialDataWithStorage(defaultData) {
  result = {};
  for (const [name, valueDefault] of Object.entries(defaultData)) {
    const strVal = localStorage.getItem(name);
    if (strVal) {
      const valueStorage = JSON.parse(strVal);
      console_log(`from storage: ${name} = ${strVal}`);
      result[name] = valueStorage;
    } else {
      result[name] = valueDefault;
    }
  }
  return result;
}

/**
 *
 * @param {*} key
 * @param {*} value
 */
function saveLocalStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

export {
  isDifferent,
  console_log,
  getInitialDataWithStorage,
  saveLocalStorage,
};
