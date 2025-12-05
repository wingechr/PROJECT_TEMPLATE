import React from "react";
import ReactDOM from "react-dom/client";
import "./index.scss";
import App from "./App.mjs";

const VERSION = "0.0.0";

const root = ReactDOM.createRoot(document.getElementById("app"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
