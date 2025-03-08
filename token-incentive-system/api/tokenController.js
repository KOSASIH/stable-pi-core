const express = require('express');
const router = express.Router();
const Web3 = require('web3');
const { abi: TokenIncentiveABI } = require('../build/contracts/TokenIncentive.json');
require('dotenv').config();

const web3 = new Web3(new Web3.providers.HttpProvider(process.env.INFURA_URL));
const tokenIncentiveAddress = process.env.TOKEN_INCENTIVE_ADDRESS;
const tokenIncentive = new web3.eth.Contract(TokenIncentiveABI, tokenIncentiveAddress);

// Get token balance
router.get('/:address/balance', async (req, res) => {
    try {
        const balance = await tokenIncentive.methods.balanceOf(req.params.address).call();
        res.json({ balance: web3.utils.fromWei(balance, 'ether') });
    } catch (error) {
        console.error("Error fetching token balance:", error);
        res.status(500).json({ error: 'Error fetching token balance' });
    }
});

// Get token allowance
router.get('/:owner/allowance/:spender', async (req, res) => {
    try {
        const allowance = await tokenIncentive.methods.allowance(req.params.owner, req.params.spender).call();
        res.json({ allowance: web3.utils.fromWei(allowance, 'ether') });
    } catch (error) {
        console.error("Error fetching token allowance:", error);
        res.status(500).json({ error: 'Error fetching token allowance' });
    }
});

// Mint tokens (only for the owner)
router.post('/mint', async (req, res) => {
    const { amount, to, from } = req.body;
    try {
        const amountInWei = web3.utils.toWei(amount, 'ether');
        
        // Call the mint function on the TokenIncentive contract
        const gasEstimate = await tokenIncentive.methods.mint(to, amountInWei).estimateGas({ from });
        const result = await tokenIncentive.methods.mint(to, amountInWei).send({ from, gas: gasEstimate });
        
        res.json({ transactionHash: result.transactionHash });
    } catch (error) {
        console.error("Error minting tokens:", error);
        res.status(500).json({ error: 'Error minting tokens' });
    }
});

module.exports = router;
