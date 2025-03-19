const express = require('express');
const router = express.Router();
const Web3 = require('web3');
const { abi: TokenIncentiveABI } = require('../build/contracts/TokenIncentive.json');
const { abi: StakingContractABI } = require('../build/contracts/StakingContract.json');
require('dotenv').config();

const web3 = new Web3(new Web3.providers.HttpProvider(process.env.INFURA_URL));
const tokenIncentiveAddress = process.env.TOKEN_INCENTIVE_ADDRESS;
const stakingContractAddress = process.env.STAKING_CONTRACT_ADDRESS;

const tokenIncentive = new web3.eth.Contract(TokenIncentiveABI, tokenIncentiveAddress);
const stakingContract = new web3.eth.Contract(StakingContractABI, stakingContractAddress);

// Get user balance
router.get('/:address/balance', async (req, res) => {
    try {
        const balance = await tokenIncentive.methods.balanceOf(req.params.address).call();
        res.json({ balance: web3.utils.fromWei(balance, 'ether') });
    } catch (error) {
        console.error("Error fetching balance:", error);
        res.status(500).json({ error: 'Error fetching balance' });
    }
});

// Get user staking balance
router.get('/:address/staking-balance', async (req, res) => {
    try {
        const stakingBalance = await stakingContract.methods.stakingBalance(req.params.address).call();
        res.json({ stakingBalance: web3.utils.fromWei(stakingBalance, 'ether') });
    } catch (error) {
        console.error("Error fetching staking balance:", error);
        res.status(500).json({ error: 'Error fetching staking balance' });
    }
});

// Get user token allowance for staking
router.get('/:address/allowance', async (req, res) => {
    try {
        const allowance = await tokenIncentive.methods.allowance(req.params.address, stakingContractAddress).call();
        res.json({ allowance: web3.utils.fromWei(allowance, 'ether') });
    } catch (error) {
        console.error("Error fetching allowance:", error);
        res.status(500).json({ error: 'Error fetching allowance' });
    }
});

module.exports = router;
