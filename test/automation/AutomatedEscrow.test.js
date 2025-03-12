// test/automation/AutomatedEscrow.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AutomatedEscrow", function () {
    let AutomatedEscrow;
    let automatedEscrow;
    let owner;
    let addr1;
    let addr2;
    let piCoin;

    beforeEach(async function () {
        [owner, addr1, addr2] = await ethers.getSigners();

        // Deploy a mock ERC20 token (PiCoin)
        const PiCoin = await ethers.getContractFactory("MockERC20");
        piCoin = await PiCoin.deploy("PiCoin", "PI", ethers.utils.parseUnits("100000000000", 18));
        await piCoin.deployed();

        // Deploy the AutomatedEscrow contract
        AutomatedEscrow = await ethers.getContractFactory("AutomatedEscrow");
        automatedEscrow = await AutomatedEscrow.deploy();
        await automatedEscrow.deployed();
    });

    it("should allow funds to be deposited into escrow", async function () {
        await piCoin.approve(automatedEscrow.address, ethers.utils.parseUnits("100", 18));
        await automatedEscrow.deposit(addr1.address, ethers.utils.parseUnits("100", 18));
        const balance = await automatedEscrow.getBalance(addr1.address);
        expect(balance).to.equal(ethers.utils.parseUnits("100", 18));
    });

    it("should allow funds to be released from escrow", async function () {
        await piCoin.approve(automatedEscrow.address, ethers.utils.parseUnits("100", 18));
        await automatedEscrow.deposit(addr1.address, ethers.utils.parseUnits("100", 18));
        await automatedEscrow.release(addr1.address, ethers.utils.parseUnits("100", 18));
        const balance = await automatedEscrow.getBalance(addr1.address);
        expect(balance).to.equal(0);
    });

    it("should not allow release of more funds than deposited", async function () {
        await piCoin.approve(automatedEscrow.address, ethers.utils.parseUnits("100", 18));
        await automatedEscrow.deposit(addr1.address, ethers.utils.parseUnits("100", 18));
        await expect(automatedEscrow.release(addr1.address, ethers.utils.parseUnits("200", 18))).to.be.revertedWith("Insufficient balance");
    });
});
