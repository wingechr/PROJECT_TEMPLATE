import { assert } from "chai";
import { describe, it } from "mocha";
import { app } from "../main.js";

describe("App", () => {
  it("can be loaded without UI", () => {
    assert.isTrue(typeof app !== "undefined");
  });
});
