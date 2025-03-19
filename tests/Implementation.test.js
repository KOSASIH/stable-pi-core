// tests/Implementation.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Implementation Contract", function () {
    let Implementation, implementation;

    beforeEach(async function () {
        Implementation = await ethers.getContractFactory("Implementation");
        implementation = await Implementation.deploy();
        await implementation.deployed();
    });

    it("should set and get value correctly", async function () {
        await implementation.setValue(42);
        const value = await implementation.getValue();
        expect(value).to.equal(42);
    });

    it("should increment value correctly", async function () {
        await implementation.setValue(10);
        await implementation.incrementValue();
        const value = await implementation.getValue();
        expect(value).to.equal(11);
    });

    it("should decrement value correctly", async function () {
        await implementation.setValue(10);
        await implementation.decrementValue();
        const value = await implementation.getValue();
        expect(value).to.equal(9);
    });

    it("should reset value to zero", async function () {
        await implementation.setValue(10);
        await implementation.resetValue();
        const value = await implementation.getValue();
        expect(value).to.equal(0);
    });
});
