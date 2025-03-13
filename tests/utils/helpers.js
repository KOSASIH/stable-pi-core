// utils/helpers.js

const Web3 = require('web3');
const { artifacts } = require('hardhat');

const web3 = new Web3();

async function getAccounts() {
    return await web3.eth.getAccounts();
}

async function deployContract(contractName, ...args) {
    const Contract = await artifacts.require(contractName);
    const instance = await Contract.new(...args);
    return instance;
}

async function getBalance(address) {
    return await web3.eth.getBalance(address);
}

async function sendEther(from, to, amount) {
    return await web3.eth.sendTransaction({ from, to, value: amount });
}

module.exports = {
    getAccounts,
    deployContract,
    getBalance,
    sendEther,
};
