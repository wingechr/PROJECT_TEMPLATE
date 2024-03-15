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
 * @param {object} initialData
 */
function addDataNodes(dg, initialData) {
  for (const name in initialData) {
    dg.addNode(name);
  }
}

/**
 *
 * @param {DataGraph} dg
 * @param {array} functionData
 */
function addFunctionNodes(dg, functionData) {
  for (const { name, dependencies, callable } of functionData) {
    dg.addFunction(name, dependencies, callable);
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
  for (const row of appUI) {
    row.component.createDynamic(document); // already done in precompile
    row.component.init(document, app);

    // also bind storage
    if (row.component.nameSet) {
      app.addCallback([row.component.nameSet], (value) =>
        saveLocalStorage(row.component.nameSet, value),
      );
    }
  }

  initialData = getInitialDataWithStorage(appDefaultData); // only in UI
  window.app = app; // export to browser
}

console_log("INIT DATA");
app.setData(initialData);

console_log("READY");

export { app };
