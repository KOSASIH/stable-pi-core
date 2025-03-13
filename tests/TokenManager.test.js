const TokenManager = artifacts.require("TokenManager");
const { expect } = require("chai");

contract("TokenManager", (accounts) => {
    let tokenManager;

    before(async () => {
        tokenManager = await TokenManager.new();
    });

    describe("Deployment", () => {
        it("should deploy the TokenManager contract successfully", async () => {
            expect(tokenManager.address).to.not.be.undefined;
        });
    });

    describe("Token Management", () => {
        it("should allow adding a new token", async () => {
            await tokenManager.addToken("TokenA", "TKA", 18, { from: accounts[0] });
            const token = await tokenManager.getToken("TokenA");
            expect(token.symbol).to.equal("TKA");
        });

        it("should allow removing a token", async () => {
            await tokenManager.removeToken("TokenA", { from: accounts[0] });
            const token = await tokenManager.getToken("TokenA");
            expect(token).to.be.undefined; // Assuming getToken returns undefined if token doesn't exist
        });
    });
});
