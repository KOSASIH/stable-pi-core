// tests/TokenIncentive.test.js

const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('TokenIncentive Contract', function () {
    let TokenIncentive;
    let token;
    let owner;
    let addr1;
    let addr2;

    beforeEach(async function () {
        TokenIncentive = await ethers.getContractFactory('TokenIncentive');
        token = await TokenIncentive.deploy();
        [owner, addr1, addr2] = await ethers.getSigners();
    });

    it('Should mint initial supply to the owner', async function () {
        const ownerBalance = await token.balanceOf(owner.address);
        expect(await token.totalSupply()).to.equal(ownerBalance);
    });

    it('Should allow users to stake tokens', async function () {
        await token.transfer(addr1.address, ethers.utils.parseEther('100'));
        await token.connect(addr1).stake(ethers.utils.parseEther('50'));
        expect(await token.stakingBalance(addr1.address)).to.equal(ethers.utils.parseEther('50'));
    });

    it('Should allow users to unstake tokens and claim rewards', async function () {
        await token.transfer(addr1.address, ethers.utils.parseEther('100'));
        await token.connect(addr1).stake(ethers.utils.parseEther('50'));
        
        // Simulate time passing
        await ethers.provider.send('evm_increaseTime', [3600]); // 1 hour
        await ethers.provider.send('evm_mine'); // Mine a new block

        const initialBalance = await token.balanceOf(addr1.address);
        await token.connect(addr1).unstake();
        
        const finalBalance = await token.balanceOf(addr1.address);
        expect(finalBalance).to.be.gt(initialBalance); // User should have more tokens after unstaking
    });

    it('Should allow the owner to change the reward rate', async function () {
        await token.setRewardRate(ethers.utils.parseEther('2'));
        expect(await token.rewardRate()).to.equal(ethers.utils.parseEther('2'));
    });
});
