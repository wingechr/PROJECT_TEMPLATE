"use strict";

import {
  console_log,
  getInitialDataWithStorage,
  saveLocalStorage,
} from "./utils.mjs";
import { DataGraph } from "./dataGraph.mjs";

class App {
  constructor(data, functions, ui) {
    let initialData = data;

    /* create app without UI */
    console_log("INIT APP");
    const graph = new DataGraph();

    // add data nodes
    for (const name in initialData) {
      graph.addNode(name);
    }

    // add functions
    for (const { name, dependencies, callable } of functions) {
      graph.addFunction(name, dependencies, callable);
    }

    // if browser
    if (typeof window !== "undefined") {
      console_log("INIT UI");
      for (const row of ui) {
        row.component.createDynamic(document); // already done in precompile
        row.component.init(document, graph);

        // also bind storage
        if (row.component.nameSet) {
          graph.addCallback([row.component.nameSet], (value) =>
            saveLocalStorage(row.component.nameSet, value),
          );
        }
      }

      initialData = getInitialDataWithStorage(data); // only in UI
      window.app = this; // export to browser
    }

    console_log("INIT DATA");
    graph.setData(initialData);

    console_log("READY");
  }
}

export { App };
