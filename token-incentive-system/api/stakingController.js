const express = require('express');
const router = express.Router();
const Web3 = require('web3');
const { abi: StakingContractABI } = require('../build/contracts/StakingContract.json');
require('dotenv').config();

const web3 = new Web3(new Web3.providers.HttpProvider(process.env.INFURA_URL));
const stakingContractAddress = process.env.STAKING_CONTRACT_ADDRESS;
const stakingContract = new web3.eth.Contract(StakingContractABI, stakingContractAddress);

// Stake tokens
router.post('/stake', async (req, res) => {
    const { amount, from } = req.body;
    try {
        // Convert amount to Wei
        const amountInWei = web3.utils.toWei(amount, 'ether');

        // Approve the staking contract to spend tokens
        const tokenIncentiveAddress = process.env.TOKEN_INCENTIVE_ADDRESS;
        const tokenIncentive = new web3.eth.Contract(require('../build/contracts/TokenIncentive.json').abi, tokenIncentiveAddress);
        await tokenIncentive.methods.approve(stakingContractAddress, amountInWei).send({ from });

        // Stake tokens
        const gasEstimate = await stakingContract.methods.stake(amountInWei).estimateGas({ from });
        const result = await stakingContract.methods.stake(amountInWei).send({ from, gas: gasEstimate });
        res.json({ transactionHash: result.transactionHash });
    } catch (error) {
        console.error("Error staking tokens:", error);
        res.status(500).json({ error: 'Error staking tokens' });
    }
});

// Unstake tokens
router.post('/unstake', async (req, res) => {
    const { from } = req.body;
    try {
        const gasEstimate = await stakingContract.methods.unstake().estimateGas({ from });
        const result = await stakingContract.methods.unstake().send({ from, gas: gasEstimate });
        res.json({ transactionHash: result.transactionHash });
    } catch (error) {
        console.error("Error unstaking tokens:", error);
        res.status(500).json({ error: 'Error unstaking tokens' });
    }
});

// Get staking balance
router.get('/:address/balance', async (req, res) => {
    try {
        const stakingBalance = await stakingContract.methods.stakingBalance(req.params.address).call();
        res.json({ stakingBalance: web3.utils.fromWei(stakingBalance, 'ether') });
    } catch (error) {
        console.error("Error fetching staking balance:", error);
        res.status(500).json({ error: 'Error fetching staking balance' });
    }
});

// Get staking rewards
router.get('/:address/rewards', async (req, res) => {
    try {
        const rewards = await stakingContract.methods.calculateReward(req.params.address).call();
        res.json({ rewards: web3.utils.fromWei(rewards, 'ether') });
    } catch (error) {
        console.error("Error fetching staking rewards:", error);
        res.status(500).json({ error: 'Error fetching staking rewards' });
    }
});

module.exports = router;
