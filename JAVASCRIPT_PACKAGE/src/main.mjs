class MyClass {
  constructor(data) {
    this.data = data;
  }

  add(value) {
    console.log("adding");
    /** I am a comment **/
    return this.data + value;
  }
}

export const Main = {
  sum: (a, b) => new MyClass(a).add(b),
};
