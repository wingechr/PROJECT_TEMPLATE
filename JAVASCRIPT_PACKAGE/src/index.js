import { Main } from "./main.mjs";

(function init(global) {
  // Attach the package to the global window object
  global.Main = Main;
})(typeof window !== "undefined" ? window : this);
