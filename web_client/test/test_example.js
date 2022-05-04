"use strict";

/*
 *  test with node_modules/.bin/mocha
 */

const chai = require("chai");
chai.use(require("chai-almost")());

let main = require('./build/js/main.js');

describe('Example', function() {
  it("Example", function() {
    chai.expect(main.plusOne(1)).to.be.almost.equals(2);
  });
});
