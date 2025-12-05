const VERSION = "0.0.0";

class MyClass {
  constructor(data) {
    this.data = data;
  }

  add(value) {
    console.log("adding");
    /** I am a comment */
    return this.data + value;
  }
}

/**
 *
 * @returns {object}
 */
function getInfo() {
  return { version: VERSION };
}

export const Main = {
  sum: (a, b) => new MyClass(a).add(b),
  getInfo: getInfo,
};
