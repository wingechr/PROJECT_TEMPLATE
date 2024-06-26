import { expect, use } from "chai";
import chaiAlmost from "chai-almost";
import { describe, it } from "mocha";
import { fileURLToPath } from "url";
import path from "path";
/* simulate DOM
import Storage from "dom-storage";
import { JSDOM } from "jsdom";
*/

import { Main } from "../src/main.mjs";

use(chaiAlmost(0.0001));

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log(__dirname);

describe("Main.sum", () => {
  it("should work", () => {
    expect(Main.sum(1, 0.99999)).to.almost.equal(2);
  });
});
