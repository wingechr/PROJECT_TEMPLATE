import { expect, use } from "chai";
import chaiAlmost from "chai-almost";
import { describe, it } from "mocha";
import { fileURLToPath } from "url";
import path from "path";

import { Main } from "../javascript_package/index.mjs";

use(chaiAlmost(0.0001));

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log(__dirname);

describe("Main", () => {
  it("sum should work", () => {
    expect(Main.sum(1, 0.99999)).to.almost.equal(2);
  });
  it("should have version", () => {
    expect(Main.getInfo()["version"]).is.not.undefined;
  });
});
