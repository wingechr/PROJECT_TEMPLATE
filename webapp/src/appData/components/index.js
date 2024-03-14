class Component {
  constructor(options) {
    this.id = options.id;
    this.parentId = options.parentId;
  }

  init(app) {
    console.log("init component");
  }
}

class LabelOUtputComponent extends Component {
  constructor(options) {
    super(options);
    this.name = options.name;
  }

  init(app) {
    let element = document.createElement("label");
    element.id = this.id;
    const dataName = this.name;

    document.getElementById(this.parentId).appendChild(element);

    app.addCallback([dataName], (value) => {
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
    this.name = options.name;
  }

  init(app) {
    let element = document.createElement("input");
    element.id = this.id;
    element.type = "number";
    element.min = this.min;
    element.max = this.max;
    const dataName = this.name;
    document.getElementById(this.parentId).appendChild(element);

    element.addEventListener("change", function (_event) {
      const value = parseInt(element.value);
      // TODO: OR: set data attribute
      app.setValue(dataName, value);
    });

    app.addCallback([dataName], (value) => {
      element.value = value;
    });
  }
}

export { Component, IntInputComponent, LabelOUtputComponent };
