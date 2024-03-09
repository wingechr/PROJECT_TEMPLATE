"use strict";

import {
  console_log,
  getInitialDataWithStorage,
  saveLocalStorage,
} from "./app/utils.js";
import { DataGraph } from "./app/dataGraph.js";
// import $ from "jquery";
import appDefaultData from "./appData/build/data.js";
import appFunctions from "./appData/build/functions.js";
import appUI from "./appData/build/ui.js";

/**
 *
 * @param {DataGraph} dg
 * @param {object} data
 */
function addDataNodes(dg, initialData) {
  for (const name in initialData) {
    dg.addNode(name);
  }
}

/**
 *
 * @param {DataGraph} dg
 * @param {array} functions
 */
function addFunctionNodes(dg, functionData) {
  for (const { name, dependencies, callable } of functionData) {
    dg.addFunction(name, dependencies, callable);
  }
}

function addHtml(uiData) {
  for (const { id, parentId, html } of uiData) {
    const parent = document.getElementById(parentId);
    // create new container element
    const elementContainer = document.createElement("div");
    // add content
    elementContainer.innerHTML = html;
    // assuming its only one item: get first child
    const element = elementContainer.firstChild;
    // assign id
    element.id = id;
    parent.appendChild(element);
  }
}

/**
 *
 * @param {DataGraph} dg
 */
function bindUICallbacks(dg, uiData) {
  for (const { id, name, getValue, setValue } of uiData) {
    const element = document.getElementById(id);

    /* change of UI => data (inputs only) */
    if (getValue) {
      element.addEventListener("change", function (_event) {
        const value = getValue(element);
        dg.setValue(name, value);
      });
    }

    /* change of data => save in storage (inputs only)*/
    if (getValue) {
      dg.addCallback([name], (value) => saveLocalStorage(name, value));
    }

    /* change of data => UI (outputs and inputs) */
    if (setValue) {
      dg.addCallback([name], (value) => setValue(element, value));
      // if data is already initialized: set values on init
      // setValue(element, dg.getValue(name));
    }
  }
}

/* create app without UI */
console_log("INIT APP");
const app = new DataGraph();
addDataNodes(app, appDefaultData);
addFunctionNodes(app, appFunctions);
let initialData = appDefaultData;

if (typeof window !== "undefined") {
  console_log("INIT UI");
  addHtml(appUI);
  bindUICallbacks(app, appUI);
  initialData = getInitialDataWithStorage(appDefaultData); // only in UI
  window.app = app; // export to browser
}

console_log("INIT DATA");
app.setData(initialData);

console_log("READY");

export { app };
