const AMM = artifacts.require("AMM");
const { expect } = require("chai");

contract("AMM", (accounts) => {
    let amm;

    before(async () => {
        amm = await AMM.new();
    });

    describe("Deployment", () => {
        it("should deploy the AMM contract successfully", async () => {
            expect(amm.address).to.not.be.undefined;
        });
    });

    describe("Liquidity Management", () => {
        it("should allow adding liquidity", async () => {
            await amm.addLiquidity(web3.utils.toWei("10", "ether"), { from: accounts[1] });
            const liquidity = await amm.getLiquidity(accounts[1]);
            expect(liquidity.toString()).to.equal(web3.utils.toWei("10", "ether"));
        });

        it("should allow removing liquidity", async () => {
            await amm.removeLiquidity(web3.utils.toWei("5", "ether"), { from: accounts[1] });
            const liquidity = await amm.getLiquidity(accounts[1]);
            expect(liquidity.toString()).to.equal(web3.utils.toWei("5", "ether"));
        });
    });
});
