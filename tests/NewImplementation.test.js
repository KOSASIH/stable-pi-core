// tests/NewImplementation.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("New Implementation Contract", function () {
    let NewImplementation, newImplementation;

    beforeEach(async function () {
        NewImplementation = await ethers.getContractFactory("NewImplementation");
        newImplementation = await NewImplementation.deploy();
        await newImplementation.deployed();
    });

    it("should set and get value correctly", async function () {
        await newImplementation.setValue(42);
        const value = await newImplementation.getValue();
        expect(value).to.equal(42);
    });

    it("should multiply value correctly", async function () {
        await newImplementation.setValue(10);
        await newImplementation.multiplyValue(2);
        const value = await newImplementation.getValue();
        expect(value).to.equal(20);
    });

    it("should divide value correctly", async function () {
        await newImplementation.setValue(20);
        await newImplementation.divideValue(2);
        const value = await newImplementation.getValue();
        expect(value).to.equal(10);
    });

    it("should square value correctly", async function () {
        await newImplementation.setValue(3);
        await newImplementation.squareValue();
        const value = await newImplementation.getValue();
        expect(value).to.equal(9);
    });
});
