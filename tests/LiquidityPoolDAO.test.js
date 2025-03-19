// tests/LiquidityPoolDAO.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("LiquidityPoolDAO", function () {
    let LiquidityPoolDAO, liquidityPoolDAO, Token, token;

    beforeEach(async function () {
        Token = await ethers.getContractFactory("GovernanceToken");
        token = await Token.deploy();
        await token.deployed();

        const LiquidityPool = await ethers.getContractFactory("LiquidityPool");
        const liquidityPool = await LiquidityPool.deploy(token.address, token.address);
        await liquidityPool.deployed();

        LiquidityPoolDAO = await ethers.getContractFactory("LiquidityPoolDAO");
        liquidityPoolDAO = await LiquidityPoolDAO.deploy(token.address, liquidityPool.address);
        await liquidityPoolDAO.deployed();
    });

    it("should create a proposal", async function () {
        await liquidityPoolDAO.createProposal("Change fee structure");
        const proposal = await liquidityPoolDAO.getProposal(0);
        expect(proposal.description).to.equal("Change fee structure");
    });

    it("should allow voting on a proposal", async function () {
        await liquidityPoolDAO.createProposal("Change fee structure");
        await token.mint(await liquidityPoolDAO.signer.getAddress(), ethers.utils.parseEther("100"));
        await token.approve(liquidityPoolDAO.address, ethers.utils.parseEther("100"));
        await liquidityPoolDAO.vote(0, true);

        const proposal = await liquidityPoolDAO.getProposal(0);
        expect(proposal.votesFor).to.equal(ethers.utils.parseEther("100"));
    });

    it("should execute a proposal if approved", async function () {
        await liquidityPoolDAO.createProposal("Change fee structure");
        await token.mint(await liquidityPoolDAO.signer.getAddress(), ethers.utils.parseEther("100"));
        await token.approve(liquidityPoolDAO.address, ethers.utils.parseEther("100"));
        await liquidityPoolDAO.vote(0, true);

        await liquidityPoolDAO.executeProposal(0);
        const proposal = await liquidityPoolDAO.getProposal(0);
        expect(proposal.executed).to.be.true;
    });
});
