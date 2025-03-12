// tests/governance/VotingMechanism.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("VotingMechanism", function () {
    let VotingMechanism;
    let votingMechanism;
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

        // Deploy the VotingMechanism contract
        VotingMechanism = await ethers.getContractFactory("VotingMechanism");
        votingMechanism = await VotingMechanism.deploy();
        await votingMechanism.deployed();
    });

    it("should allow users to vote on a proposal", async function () {
        await votingMechanism.vote(1, addr1.address, true); // Vote 'yes'
        const vote = await votingMechanism.getVote(1, addr1.address);
        expect(vote.voteChoice).to.be.true;
        expect(vote.hasVoted).to.be.true;
    });

    it("should not allow double voting", async function () {
        await votingMechanism.vote(1, addr1.address, true); // Vote 'yes'
        await expect(votingMechanism.vote(1, addr1.address, false)).to.be.revertedWith("Voter has already voted");
    });

    it("should allow delegation of votes", async function () {
        await votingMechanism.delegateVote(addr2.address);
        const delegate = awaitvotingMechanism.getDelegate(addr1.address);
        expect(delegate).to.equal(addr2.address);
    });

    it("should not allow delegation to self", async function () {
        await expect(votingMechanism.delegateVote(owner.address)).to.be.revertedWith("Cannot delegate to self");
    });

    it("should allow users to retrieve their voting history", async function () {
        await votingMechanism.vote(1, addr1.address, true); // Vote 'yes'
        const history = await votingMechanism.getVotingHistory(addr1.address);
        expect(history.length).to.equal(1);
        expect(history[0].proposalId).to.equal(1);
        expect(history[0].voteChoice).to.be.true;
    });
});
