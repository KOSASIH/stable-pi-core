// scripts/utils/tokenUtils.js

const Web3 = require('web3');
const ERC20ABI = require('./ERC20ABI.json'); // Import the ERC20 ABI

async function transferToken(tokenAddress, fromAddress, toAddress, amount, web3) {
    const tokenContract = new web3.eth.Contract(ERC20ABI, tokenAddress);
    const transferAmount = web3.utils.toWei(amount.toString(), 'ether');

    try {
        const tx = await tokenContract.methods.transfer(toAddress, transferAmount).send({ from: fromAddress });
        console.log(`Transferred ${amount} tokens from ${fromAddress} to ${toAddress}. Transaction hash: ${tx.transaction hash}`);
    } catch (error) {
        console.error('Token transfer failed:', error);
        throw error;
    }
}

async function getTokenBalance(tokenAddress, account, web3) {
    const tokenContract = new web3.eth.Contract(ERC20ABI, tokenAddress);
    const balance = await tokenContract.methods.balanceOf(account).call();
    return web3.utils.fromWei(balance, 'ether');
}

module.exports = { transferToken, getTokenBalance }; ### 1. `deploy.js`

This script deploys the smart contracts to the Ethereum network using Truffle.

```javascript
// scripts/deploy.js

const Web3 = require('web3');
const HDWalletProvider = require('@truffle/hdwallet-provider');
const MultiAssetCollateral = artifacts.require('MultiAssetCollateral');
const AMM = artifacts.require('AMM');
const TokenManager = artifacts.require('TokenManager');

const provider = new HDWalletProvider(process.env.MNEMONIC, process.env.INFURA_URL);
const web3 = new Web3(provider);

async function deployContracts() {
    const accounts = await web3.eth.getAccounts();
    console.log('Deploying contracts with account:', accounts[0]);

    // Deploy MultiAssetCollateral
    const collateralInstance = await MultiAssetCollateral.new();
    console.log('MultiAssetCollateral deployed at:', collateralInstance.address);

    // Deploy AMM
    const ammInstance = await AMM.new(collateralInstance.address);
    console.log('AMM deployed at:', ammInstance.address);

    // Deploy TokenManager
    const tokenManagerInstance = await TokenManager.new();
    console.log('TokenManager deployed at:', tokenManagerInstance.address);

    provider.engine.stop();
}

deployContracts()
    .then(() => console.log('Deployment complete.'))
    .catch(err => console.error('Deployment failed:', err));
