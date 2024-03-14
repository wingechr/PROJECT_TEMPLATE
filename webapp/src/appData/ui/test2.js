"use strict";
import { Component, LabelOUtputComponent } from "./../components/index.js";

const c1 = new LabelOUtputComponent({
  id: "id2",
  parentId: "main",
  name: "f2",
});
const c2 = new Component({ id: "id3", parentId: "id1" });
export { c1, c2 as c3 };
