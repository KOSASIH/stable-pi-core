// tests/Proxy.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Proxy Contract", function () {
    let Proxy, proxy, Implementation, implementation;

    beforeEach(async function () {
        Implementation = await ethers.getContractFactory("Implementation");
        implementation = await Implementation.deploy();
        await implementation.deployed();

        Proxy = await ethers.getContractFactory("Proxy");
        proxy = await Proxy.deploy(implementation.address);
        await proxy.deployed();
    });

    it("should delegate calls to the implementation contract", async function () {
        const setValueTx = await proxy.setValue(42);
        await setValueTx.wait();

        const value = await proxy.getValue();
        expect(value).to.equal(42);
    });

    it("should upgrade the implementation contract", async function () {
        const NewImplementation = await ethers.getContractFactory("NewImplementation");
        const newImplementation = await NewImplementation.deploy();
        await newImplementation.deployed();

        const upgradeTx = await proxy.upgrade(newImplementation.address);
        await upgradeTx.wait();

        const setValueTx = await proxy.setValue(100);
        await setValueTx.wait();

        const value = await proxy.getValue();
        expect(value).to.equal(100);
    });
});
