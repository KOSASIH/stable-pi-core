// scripts/test.js

const { expect } = require("chai");
const { ethers, upgrades } = require("hardhat");

describe("PiConverter", function () {
    let piConverter;
    let owner;
    let addr1;
    let addr2;

    const initialRate = 100; // Initial conversion rate
    const initialFeePercentage = 2; // Initial fee percentage
    const feeCollector = "0xYourFeeCollectorAddress"; // Replace with a valid address

    beforeEach(async function () {
        [owner, addr1, addr2] = await ethers.getSigners();

        // Deploy the PiConverter contract
        const PiConverter = await ethers.getContractFactory("PiConverter");
        piConverter = await upgrades.deployProxy(PiConverter, [initialRate, initialFeePercentage, feeCollector], { initializer: 'initialize' });
        await piConverter.deployed();
    });

    it("Should deploy the contract with correct initial parameters", async function () {
        expect(await piConverter.rate()).to.equal(initialRate);
        expect(await piConverter.feePercentage()).to.equal(initialFeePercentage);
        expect(await piConverter.feeCollector()).to.equal(feeCollector);
    });

    it("Should calculate the correct conversion fee", async function () {
        const amount = ethers.utils.parseUnits("100", 18); // 100 tokens
        const expectedFee = (amount.mul(initialFeePercentage)).div(100);
        const expectedAmountAfterFee = amount.sub(expectedFee);

        const fee = await piConverter.calculateFee(amount);
        expect(fee).to.equal(expectedFee);

        const amountAfterFee = await piConverter.convert(amount);
        expect(amountAfterFee).to.equal(expectedAmountAfterFee);
    });

    it("Should only allow the owner to update the fee collector", async function () {
        await expect(piConverter.connect(addr1).updateFeeCollector(addr2.address)).to.be.revertedWith("Not the owner");
        await piConverter.updateFeeCollector(addr2.address);
        expect(await piConverter.feeCollector()).to.equal(addr2.address);
    });

    it("Should revert if the fee percentage is out of bounds", async function () {
        await expect(piConverter.updateFeePercentage(101)).to.be.revertedWith("Fee percentage must be between 0 and 100");
        await expect(piConverter.updateFeePercentage(-1)).to.be.revertedWith("Fee percentage must be between 0 and 100");
    });

    it("Should allow emergency withdrawal by the owner", async function () {
        const amount = ethers.utils.parseUnits("10", 18); // 10 tokens
        await piConverter.connect(owner).emergencyWithdraw(feeCollector, amount);
        // Add assertions to check the balance after withdrawal
    });

    it("Should emit an event when the fee collector is updated", async function () {
        await expect(piConverter.updateFeeCollector(addr2.address))
            .to.emit(piConverter, "FeeCollectorUpdated")
            .withArgs(addr2.address);
    });
});
