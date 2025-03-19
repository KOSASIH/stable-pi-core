// integration.test.js
require('dotenv').config();
const { expect } = require('chai');
const { ethers, upgrades } = require('hardhat');

describe("CrossChainBridge Integration Tests", function () {
    let bridge;
    let owner;
    let user;
    const chainId1 = 1; // Mainnet
    const chainId2 = 2; // Testnet or another chain
    const tokenAmount = ethers.utils.parseEther("10"); // Amount to transfer

    before(async function () {
        // Get signers
        [owner, user] = await ethers.getSigners();

        // Deploy the CrossChainBridge contract
        const Bridge = await ethers.getContractFactory("CrossChainBridge");
        bridge = await upgrades.deployProxy(Bridge, [/* constructor arguments */], { initializer: 'initialize' });
        await bridge.deployed();
    });

    it("should allow user to deposit tokens for cross-chain transfer", async function () {
        // Simulate user approving the bridge to spend tokens
        await bridge.connect(user).approve(bridge.address, tokenAmount);
        
        // User deposits tokens into the bridge
        await bridge.connect(user).deposit(chainId2, tokenAmount);

        // Check the user's balance in the bridge
        const bridgeBalance = await bridge.balanceOf(user.address);
        expect(bridgeBalance).to.equal(tokenAmount);
    });

    it("should emit a TransferInitiated event on deposit", async function () {
        await expect(bridge.connect(user).deposit(chainId2, tokenAmount))
            .to.emit(bridge, 'TransferInitiated')
            .withArgs(user.address, chainId2, tokenAmount);
    });

    it("should allow the owner to finalize the transfer on the destination chain", async function () {
        // Simulate the transfer finalization process
        await bridge.finalizeTransfer(user.address, chainId1, tokenAmount);

        // Check the user's balance after finalization
        const userBalance = await bridge.balanceOf(user.address);
        expect(userBalance).to.equal(0); // User should have 0 balance in the bridge after finalization
    });

    it("should revert if non-owner tries to finalize the transfer", async function () {
        await expect(bridge.connect(user).finalizeTransfer(user.address, chainId1, tokenAmount))
            .to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("should allow the user to withdraw tokens after finalization", async function () {
        // Simulate the user withdrawing tokens after finalization
        await bridge.connect(user).withdraw(tokenAmount);

        // Check the user's balance after withdrawal
        const userTokenBalance = await bridge.balanceOf(user.address);
        expect(userTokenBalance).to.equal(tokenAmount);
    });

    after(async function () {
        // Clean up or reset state if necessary
    });
});
