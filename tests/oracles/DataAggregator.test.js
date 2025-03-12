// tests/oracles/DataAggregator.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DataAggregator", function () {
    let DataAggregator;
    let dataAggregator;
    let owner;
    let addr1;

    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();

        // Deploy the DataAggregator contract
        DataAggregator = await ethers.getContractFactory("DataAggregator");
        dataAggregator = await DataAggregator.deploy();
        await dataAggregator.deployed();
    });

    it("should allow the owner to add data sources", async function () {
        await dataAggregator.addDataSource(addr1.address);
        const isDataSource = await dataAggregator.isDataSource(addr1.address);
        expect(isDataSource).to.be.true;
    });

    it("should not allow non-owners to add data sources", async function () {
        await expect(dataAggregator.connect(addr1).addDataSource(addr1.address)).to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("should allow data sources to submit data", async function () {
        await dataAggregator.addDataSource(addr1.address);
        await dataAggregator.connect(addr1).submitData(ethers.utils.parseUnits("300000", 18));
        const latestData = await dataAggregator.getLatestData(addr1.address);
        expect(latestData).to.equal(ethers.utils.parseUnits("300000", 18));
    });

    it("should not allow non-data sources to submit data", async function () {
        await expect(dataAggregator.connect(addr1).submitData(ethers.utils.parseUnits("300000", 18))).to.be.revertedWith("Not a data source");
    });

    it("should return the latest data correctly", async function () {
        await dataAggregator.addDataSource(addr1.address);
        await dataAggregator.connect(addr1).submitData(ethers.utils.parseUnits("300000", 18));
        const latestData = await dataAggregator.getLatestData(addr1.address);
        expect(latestData).to.equal(ethers.utils.parseUnits("300000", 18));
    });
});
