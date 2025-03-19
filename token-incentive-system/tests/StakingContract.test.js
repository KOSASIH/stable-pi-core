// tests/StakingContract.test.js

const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('StakingContract', function () {
    let StakingContract;
    let staking;
    let rewardToken;
    let owner;
    let addr1;

    beforeEach(async function () {
        const RewardToken = await ethers.getContractFactory('TokenIncentive');
        rewardToken = await RewardToken.deploy();
        StakingContract = await ethers.getContractFactory('StakingContract');
        staking = await StakingContract.deploy(rewardToken.address, ethers.utils.parseEther('1'));
        [owner, addr1] = await ethers.getSigners();

        // Mint tokens to addr1 for testing
        await rewardToken.transfer(addr1.address, ethers.utils.parseEther('100'));
    });

    it('Should allow users to stake tokens', async function () {
        await rewardToken.connect(addr1).approve(staking.address, ethers.utils.parseEther('50'));
        await staking.connect(addr1).stake(ethers.utils.parseEther('50'));
        expect(await staking.stakingBalance(addr1.address)).to.equal(ethers.utils.parseEther('50'));
    });

    it('Should allow users to unstake tokens and claim rewards', async function () {
        await rewardToken.connect(addr1).approve(staking.address, ethers.utils.parseEther('50'));
        await staking.connect(addr1).stake(ethers.utils.parseEther('50'));

        // Simulate time passing
        await ethers.provider.send('evm_increaseTime', [3600]); // 1 hour
        await ethers.provider.send('evm_mine'); // Mine a new block

        const initialBalance = await rewardToken.balanceOf(addr1.address);
        await staking.connect(addr1).unstake();
        
        const finalBalance = await rewardToken.balanceOf(addr1.address);
        expect(finalBalance).to.be.gt(initialBalance); // User should have more tokens after unstaking
    });

    it('Should allow the owner to change the reward rate', async function () {
        await staking.setRewardRate(ethers.utils.parseEther('2'));
        expect(await staking.rewardRate()).to.equal(ethers.utils.parseEther('2'));
    });

    it('Should allow emergency withdrawal', async function () {
        await rewardToken.connect(addr1).approve(staking.address, ethers.utils.parseEther(' 50'));
        await staking.connect(addr1).stake(ethers.utils.parseEther('50'));
        
        await staking.connect(addr1).emergencyWithdraw();
        expect(await staking.stakingBalance(addr1.address)).to.equal(0);
    });
});
