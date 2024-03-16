"use strict";

import { App } from "@wingechr/webapp";

import data from "./data/index.mjs";
import functions from "./functions/index.mjs";
import ui from "./ui/index.mjs";

const createStaticHtml = false; // already pre-build
export default new App(data, functions, ui, createStaticHtml);
