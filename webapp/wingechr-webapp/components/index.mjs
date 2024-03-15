import { console_log } from "./../utils.mjs";

class Component {
  constructor(options) {
    this.id = options.id;
    this.parentId = options.parentId;
  }
  createDynamic(document) {
    console_log("create dynamic html");
  }
  createStatic(document) {
    console_log("create static html");
  }
  init(document, app) {
    console_log("init component");
  }
}

class LabelOUtputComponent extends Component {
  constructor(options) {
    super(options);
    this.nameGet = options.name;
  }
  createDynamic(document) {
    let element = document.createElement("label");
    element.setAttribute("data-name-get", this.nameGet);
    element.id = this.id;
    document.getElementById(this.parentId).appendChild(element);
  }
  init(document, app) {
    let element = document.getElementById(this.id);
    const nameGet = element.getAttribute("data-name-get");

    app.addCallback([nameGet], (value) => {
      element.textContent = value.toLocaleString("de-DE", {
        useGrouping: true,
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
      });
    });
  }
}

class IntInputComponent extends Component {
  constructor(options) {
    super(options);
    this.min = options.min;
    this.max = options.max;
    this.nameGet = options.name;
    this.nameSet = options.name;
  }

  createDynamic(document) {
    let element = document.createElement("input");
    element.setAttribute("data-name-set", this.nameSet);
    element.setAttribute("data-name-get", this.nameGet);
    element.id = this.id;
    element.type = "number";
    element.min = this.min;
    element.max = this.max;
    document.getElementById(this.parentId).appendChild(element);
  }

  init(document, app) {
    let element = document.getElementById(this.id);
    const nameSet = element.getAttribute("data-name-set");
    const nameGet = element.getAttribute("data-name-get");

    element.addEventListener("change", function (_event) {
      const value = parseInt(element.value);
      // TODO: OR: set data attribute
      app.setValue(nameGet, value);
    });

    app.addCallback([nameSet], (value) => {
      element.value = value;
    });
  }
}

export { Component, IntInputComponent, LabelOUtputComponent };
