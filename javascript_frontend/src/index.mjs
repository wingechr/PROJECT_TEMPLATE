import { Main } from "@wingechr/javascript_package/javascript_package/index.mjs";

// import "../../node_modules/jquery/dist/jquery.min.js";
// import "../../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js";
// import "../../node_modules/bootstrap-select/js/bootstrap-select.js";

(function init(global) {
  // Attach the package to the global window object
  global.Main = Main;
  console.log(Main.getInfo());
})(typeof window !== "undefined" ? window : this);
