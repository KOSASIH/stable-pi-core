// test/automation/AutomatedSupplyManager.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AutomatedSupplyManager", function () {
    let AutomatedSupplyManager;
    let automatedSupplyManager;
    let owner;
    let addr1;
    let addr2;
    let piCoin;
    let priceFeed;

    beforeEach(async function () {
        [owner, addr1, addr2] = await ethers.getSigners();

        // Deploy a mock ERC20 token (PiCoin)
        const PiCoin = await ethers.getContractFactory("MockERC20");
        piCoin = await PiCoin.deploy("PiCoin", "PI", ethers.utils.parseUnits("100000000000", 18));
        await piCoin.deployed();

        // Deploy a mock price feed
        const PriceFeed = await ethers.getContractFactory("MockPriceFeed");
        priceFeed = await PriceFeed.deploy();
        await priceFeed.deployed();

        // Deploy the AutomatedSupplyManager contract
        AutomatedSupplyManager = await ethers.getContractFactory("AutomatedSupplyManager");
        automatedSupplyManager = await AutomatedSupplyManager.deploy(piCoin.address, priceFeed.address, 314159 * 10**18, 5, 3600);
        await automatedSupplyManager.deployed();
    });

    it("should adjust supply correctly when price is below target", async function () {
        await priceFeed.setPrice(300000 * 10**18); // Set price below target
        await automatedSupplyManager.adjustSupply();
        const newSupply = await piCoin.totalSupply();
        expect(newSupply).to.be.above(ethers.utils.parseUnits("100000000000", 18)); // Supply should increase
    });

    it("should adjust supply correctly when price is above target", async function () {
        await priceFeed.setPrice(320000 * 10**18); // Set price above target
        await automatedSupplyManager.adjustSupply();
        const newSupply = await piCoin.totalSupply();
        expect(newSupply).to.be.below(ethers.utils.parseUnits("100000000000", 18)); // Supply should decrease
    });

    it("should not adjust supply if cooldown period has not passed", async function () {
        await priceFeed.setPrice(300000 * 10**18); // Set price below target
        await automatedSupplyManager.adjustSupply();
        await expect(automatedSupplyManager.adjustSupply()).to.be.revertedWith("Cooldown period not met");
    });
});
