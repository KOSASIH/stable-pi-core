const Web3 = require('web3');
const PiConverterABI = require('../contracts/PiConverter.json'); // ABI of the PiConverter contract
const { toBN } = Web3.utils;

class ConversionService {
    constructor(contractAddress, providerUrl) {
        this.web3 = new Web3(new Web3.providers.HttpProvider(providerUrl));
        this.contract = new this.web3.eth.Contract(PiConverterABI, contractAddress);
    }

    async deposit(userAddress, amount, privateKey) {
        try {
            const data = this.contract.methods.deposit(toBN(amount).toString()).encodeABI();
            const gasPrice = await this.web3.eth.getGasPrice();
            const gasEstimate = await this.contract.methods.deposit(toBN(amount).toString()).estimateGas({ from: userAddress });

            const tx = {
                from: userAddress,
                to: this.contract.options.address,
                gas: gasEstimate,
                gasPrice: gasPrice,
                data: data,
            };

            const signedTx = await this.web3.eth.accounts.signTransaction(tx, privateKey);
            const receipt = await this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
            console.log(`Deposit successful: ${receipt.transactionHash}`);
            return receipt;
        } catch (error) {
            console.error(`Deposit failed: ${error.message}`);
            throw new Error('Deposit transaction failed');
        }
    }

    async convert(userAddress, amount, privateKey) {
        try {
            const data = this.contract.methods.convert(toBN(amount).toString()).encodeABI();
            const gasPrice = await this.web3.eth.getGasPrice();
            const gasEstimate = await this.contract.methods.convert(toBN(amount).toString()).estimateGas({ from: userAddress });

            const tx = {
                from: userAddress,
                to: this.contract.options.address,
                gas: gasEstimate,
                gasPrice: gasPrice,
                data: data,
            };

            const signedTx = await this.web3.eth.accounts.signTransaction(tx, privateKey);
            const receipt = await this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
            console.log(`Conversion successful: ${receipt.transactionHash}`);
            return receipt;
        } catch (error) {
            console.error(`Conversion failed: ${error.message}`);
            throw new Error('Conversion transaction failed');
        }
    }

    async checkBalance(userAddress) {
        try {
            const balance = await this.contract.methods.checkBalance().call({ from: userAddress });
            return balance;
        } catch (error) {
            console.error(`Failed to check balance: ${error.message}`);
            throw new Error('Failed to retrieve balance');
        }
    }

    async updateConversionRate(newRate, privateKey) {
        try {
            const data = this.contract.methods.updateConversionRate(toBN(newRate).toString()).encodeABI();
            const gasPrice = await this.web3.eth.getGasPrice();
            const gasEstimate = await this.contract.methods.updateConversionRate(toBN(newRate).toString()).estimateGas({ from: privateKey });

            const tx = {
                from: privateKey,
                to: this.contract.options.address,
                gas: gasEstimate,
                gasPrice: gasPrice,
                data: data,
            };

            const signedTx = await this.web3.eth.accounts.signTransaction(tx, privateKey);
            const receipt = await this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
            console.log(`Conversion rate updated: ${receipt.transactionHash}`);
            return receipt;
        } catch (error) {
            console.error(`Failed to update conversion rate: ${error.message}`);
            throw new Error('Update conversion rate transaction failed');
        }
    }
}

module.exports = ConversionService;
