const Web3 = require('web3');

class WalletService {
    constructor(providerUrl) {
        this.web3 = new Web3(new Web3.providers.HttpProvider(providerUrl));
    }

    async connectWallet() {
        if (window.ethereum) {
            try {
                // Request account access
                const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                return accounts[0]; // Return the connected account
            } catch (error) {
                console.error('User  denied account access:', error);
                throw new Error('Wallet connection failed');
            }
        } else {
            console.error('No Ethereum provider found. Install MetaMask.');
            throw new Error('No Ethereum provider found');
        }
    }

    async getBalance(address) {
        try {
            const balance = await this.web3.eth.getBalance(address);
            return this.web3.utils.fromWei(balance, 'ether'); // Convert balance from Wei to Ether
        } catch (error) {
            console.error('Failed to retrieve balance:', error);
            throw new Error('Failed to retrieve balance');
        }
    }
}

module.exports = new WalletService('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'); // Replace with your provider
