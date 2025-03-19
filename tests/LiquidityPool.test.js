// tests/LiquidityPool.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("LiquidityPool", function () {
    let LiquidityPool, liquidityPool, TokenA, tokenA, TokenB, tokenB;

    beforeEach(async function () {
        TokenA = await ethers.getContractFactory("TokenA");
        tokenA = await TokenA.deploy();
        await tokenA.deployed();

        TokenB = await ethers.getContractFactory("TokenB");
        tokenB = await TokenB.deploy();
        await tokenB.deployed();

        LiquidityPool = await ethers.getContractFactory("LiquidityPool");
        liquidityPool = await LiquidityPool.deploy(tokenA.address, tokenB.address);
        await liquidityPool.deployed();
    });

    it("should add liquidity correctly", async function () {
        await tokenA.mint(await liquidityPool.signer.getAddress(), ethers.utils.parseEther("100"));
        await tokenB.mint(await liquidityPool.signer.getAddress(), ethers.utils.parseEther("100"));

        await tokenA.approve(liquidityPool.address, ethers.utils.parseEther("100"));
        await tokenB.approve(liquidityPool.address, ethers.utils.parseEther("100"));

        await liquidityPool.addLiquidity(ethers.utils.parseEther("100"), ethers.utils.parseEther("100"));

        const [reserveA, reserveB] = await liquidityPool.getReserves();
        expect(reserveA).to.equal(ethers.utils.parseEther("100"));
        expect(reserveB).to.equal(ethers.utils.parseEther("100"));
    });

    it("should swap tokens correctly", async function () {
        await tokenA.mint(await liquidityPool.signer.getAddress(), ethers.utils.parseEther("100"));
        await tokenB.mint(await liquidityPool.signer.getAddress(), ethers.utils.parseEther("100"));

        await tokenA.approve(liquidityPool.address, ethers.utils.parseEther("100"));
        await tokenB.approve(liquidityPool.address, ethers.utils.parseEther("100"));

        await liquidityPool.addLiquidity(ethers.utils.parseEther("100"), ethers.utils.parseEther("100"));

        await tokenA.approve(liquidityPool.address, ethers.utils.parseEther("10"));
        await liquidityPool.swap(ethers.utils.parseEther("10"), true); // Swap from A to B

        const [reserveA, reserveB] = await liquidityPool.getReserves();
        expect(reserveA).to.equal(ethers.utils.parseEther("90"));
        expect(reserveB).to.be.greaterThan(ethers.utils.parseEther("100")); // Check that reserveB increased
    });
});
