// tests/StablePiCore.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("StablePiCore Contract", function () {
    let StablePiCore, stablePiCore, Proxy, proxy, NewImplementation, newImplementation;

    beforeEach(async function () {
        NewImplementation = await ethers.getContractFactory("NewImplementation");
        newImplementation = await NewImplementation.deploy();
await newImplementation.deployed();

        Proxy = await ethers.getContractFactory("Proxy");
        proxy = await Proxy.deploy(newImplementation.address);
        await proxy.deployed();

        StablePiCore = await ethers.getContractFactory("StablePiCore");
        stablePiCore = await StablePiCore.deploy(proxy.address);
        await stablePiCore.deployed();
    });

    it("should initialize with correct values", async function () {
        const initialValue = await stablePiCore.getValue();
        expect(initialValue).to.equal(0);
    });

    it("should perform conversion correctly", async function () {
        await stablePiCore.setConversionRate(2);
        const convertedValue = await stablePiCore.convert(10);
        expect(convertedValue).to.equal(20);
    });

    it("should upgrade the implementation and retain state", async function () {
        const NewImplementation2 = await ethers.getContractFactory("NewImplementation");
        const newImplementation2 = await NewImplementation2.deploy();
        await newImplementation2.deployed();

        const upgradeTx = await proxy.upgrade(newImplementation2.address);
        await upgradeTx.wait();

        await stablePiCore.setConversionRate(3);
        const convertedValue = await stablePiCore.convert(10);
        expect(convertedValue).to.equal(30);
    });

    it("should handle errors gracefully", async function () {
        await expect(stablePiCore.convert(0)).to.be.revertedWith("Conversion amount must be greater than zero");
    });
});
