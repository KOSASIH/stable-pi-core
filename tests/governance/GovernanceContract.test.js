// tests/governance/GovernanceContract.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GovernanceContract", function () {
    let GovernanceContract;
    let governanceContract;
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

        // Deploy the GovernanceContract
        GovernanceContract = await ethers.getContractFactory("GovernanceContract");
        governanceContract = await GovernanceContract.deploy(piCoin.address);
        await governanceContract.deployed();
    });

    it("should allow the owner to create a proposal", async function () {
        await governanceContract.createProposal("Proposal 1", "Description of Proposal 1");
        const proposal = await governanceContract.proposals(0);
        expect(proposal.title).to.equal("Proposal 1");
        expect(proposal.description).to.equal("Description of Proposal 1");
        expect(proposal.voteCount).to.equal(0);
    });

    it("should allow users to vote on a proposal", async function () {
        await governanceContract.createProposal("Proposal 1", "Description of Proposal 1");
        await piCoin.connect(addr1).approve(governanceContract.address, ethers.utils.parseUnits("100", 18));
        await governanceContract.connect(addr1).vote(0, true); // Vote 'yes'
        const proposal = await governanceContract.proposals(0);
        expect(proposal.voteCount).to.equal(1);
    });

    it("should not allow voting on a non-existent proposal", async function () {
        await expect(governanceContract.connect(addr1).vote(999, true)).to.be.revertedWith("Proposal does not exist");
    });

    it("should not allow double voting", async function () {
        await governanceContract.createProposal("Proposal 1", "Description of Proposal 1");
        await piCoin.connect(addr1).approve(governanceContract.address, ethers.utils.parseUnits("100", 18));
        await governanceContract.connect(addr1).vote(0, true); // Vote 'yes'
        await expect(governanceContract.connect(addr1).vote(0, false)).to.be.revertedWith("You have already voted on this proposal");
    });
});
