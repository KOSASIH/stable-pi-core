// tests/MultiAssetCollateral.test.js
const MultiAssetCollateral = artifacts.require("MultiAssetCollateral");
const { expect } = require("chai");

contract("MultiAssetCollateral", (accounts) => {
    let collateral;

    before(async () => {
        collateral = await MultiAssetCollateral.new();
    });

    describe("Deployment", () => {
        it("should deploy the contract successfully", async () => {
            expect(collateral.address).to.not.be.undefined;
        });
    });

    describe("Collateral Management", () => {
        it("should allow adding collateral", async () => {
            await collateral.addCollateral(accounts[1], web3.utils.toWei("10", "ether"));
            const balance = await collateral.getCollateral(accounts[1]);
            expect(balance.toString()).to.equal(web3.utils.toWei("10", "ether"));
        });

        it("should allow removing collateral", async () => {
            await collateral.removeCollateral(accounts[1], web3.utils.toWei("5", "ether"));
            const balance = await collateral.getCollateral(accounts[1]);
            expect(balance.toString()).to.equal(web3.utils.toWei("5", "ether"));
        });
    });
});
