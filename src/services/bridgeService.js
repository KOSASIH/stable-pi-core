const Web3 = require('web3');
const PiBridgeABI = require('../contracts/PiBridge.json'); // ABI of the PiBridge contract

class BridgeService {
    constructor(contractAddress, providerUrl) {
        this.web3 = new Web3(new Web3.providers.HttpProvider(providerUrl));
        this.contract = new this.web3.eth.Contract(PiBridgeABI, contractAddress);
    }

    async deposit(userAddress, amount) {
        const data = this.contract.methods.deposit(amount).encodeABI();
        const gasPrice = await this.web3.eth.getGasPrice();
        const gasEstimate = await this.contract.methods.deposit(amount).estimateGas({ from: userAddress });

        const tx = {
            from: userAddress,
            to: this.contract.options.address,
            gas: gasEstimate,
            gasPrice: gasPrice,
            data: data,
        };

        const signedTx = await this.web3.eth.accounts.signTransaction(tx, userAddress.privateKey);
        return this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
    }

    async withdraw(userAddress, amount) {
        const data = this.contract.methods.withdraw(amount).encodeABI();
        const gasPrice = await this.web3.eth.getGasPrice();
        const gasEstimate = await this.contract.methods.withdraw(amount).estimateGas({ from: userAddress });

        const tx = {
            from: userAddress,
            to: this.contract.options.address,
            gas: gasEstimate,
            gasPrice: gasPrice,
            data: data,
        };

        const signedTx = await this.web3.eth.accounts.signTransaction(tx, userAddress.privateKey);
        return this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
    }

    async bridge(userAddress, amount, targetChain) {
        const data = this.contract.methods.bridge(amount, targetChain).encodeABI();
        const gasPrice = await this.web3.eth.getGasPrice();
        const gasEstimate = await this.contract.methods.bridge(amount, targetChain).estimateGas({ from: userAddress });

        const tx = {
            from: userAddress,
            to: this.contract.options.address,
            gas: gasEstimate,
            gasPrice: gasPrice,
            data: data,
        };

        const signedTx = await this.web3.eth.accounts.signTransaction(tx, userAddress.privateKey);
        return this.web3.eth.sendSignedTransaction(signedTx.rawTransaction);
    }
}

module.exports = BridgeService;
