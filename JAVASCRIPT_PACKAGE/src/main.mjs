class MyClass {
  constructor(data) {
    this.data = data;
  }

  add(value) {
    return this.data + value;
  }
}

export const Main = {
  sum: (a, b) => new MyClass(a).add(b),
};
