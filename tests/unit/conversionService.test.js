const { expect } = require('chai');
const sinon = require('sinon');
const Web3 = require('web3');
const ConversionService = require('../../src/services/conversionService');
const PiConverterABI = require('../../src/contracts/PiConverter.json');

describe('ConversionService', () => {
    let conversionService;
    let mockContract;
    const contractAddress = '0x1234567890abcdef1234567890abcdef12345678';
    const providerUrl = 'http://localhost:8545'; // Mock provider URL
    const userAddress = '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef';
    const privateKey = '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef';

    beforeEach(() => {
        // Create a new instance of ConversionService before each test
        conversionService = new ConversionService(contractAddress, providerUrl);
        mockContract = sinon.stub(conversionService.contract.methods);
    });

    afterEach(() => {
        sinon.restore(); // Restore the original methods after each test
    });

    describe('deposit', () => {
        it('should successfully deposit an amount', async () => {
            const amount = 100;

            // Mock the methods
            mockContract.deposit.returns({
                encodeABI: () => 'mockedData',
                estimateGas: () => Promise.resolve(21000),
            });

            sinon.stub(Web3.utils, 'toBN').returns({
                toString: () => amount.toString(),
            });

            sinon.stub(conversionService.web3.eth.accounts, 'signTransaction').returns({
                rawTransaction: 'mockedRawTransaction',
            });

            sinon.stub(conversionService.web3.eth, 'sendSignedTransaction').returns(Promise.resolve({ transactionHash: 'mockedTransactionHash' }));

            const receipt = await conversionService.deposit(userAddress, amount, privateKey);
            expect(receipt.transactionHash).to.equal('mockedTransactionHash');
        });

        it('should throw an error if deposit fails', async () => {
            const amount = 100;

            // Mock the methods to throw an error
            mockContract.deposit.returns({
                encodeABI: () => 'mockedData',
                estimateGas: () => Promise.resolve(21000),
            });

            sinon.stub(Web3.utils, 'toBN').returns({
                toString: () => amount.toString(),
            });

            sinon.stub(conversionService.web3.eth.accounts, 'signTransaction').throws(new Error('Transaction signing failed'));

            try {
                await conversionService.deposit(userAddress, amount, privateKey);
            } catch (error) {
                expect(error.message).to.equal('Deposit transaction failed');
            }
        });
    });

    describe('convert', () => {
        it('should successfully convert an amount', async () => {
            const amount = 50;

            // Mock the methods
            mockContract.convert.returns({
                encodeABI: () => 'mockedData',
                estimateGas: () => Promise.resolve(21000),
            });

            sinon.stub(Web3.utils, 'toBN').returns({
                toString: () => amount.toString(),
            });

            sinon.stub(conversionService.web3.eth.accounts, 'signTransaction').returns({
                rawTransaction: 'mockedRawTransaction',
            });

            sinon.stub(conversionService.web3.eth, 'sendSignedTransaction').returns(Promise.resolve({ transactionHash: 'mockedTransactionHash' }));

            const receipt = await conversionService.convert(userAddress, amount, privateKey);
            expect(receipt.transactionHash).to.equal('mockedTransactionHash');
        });

        it('should throw an error if conversion fails', async () => {
            const amount = 50;

            // Mock the methods to throw an error
            mockContract.convert.returns({
                encodeABI: () => 'mockedData',
                estimateGas: () => Promise.resolve(21000),
            });

            sinon.stub(Web3.utils, 'toBN').returns({
                toString: () => amount.toString(),
            });

            sinon.stub(conversionService.web3.eth.accounts, 'signTransaction').throws(new Error('Transaction signing failed'));

            try {
                await conversionService.convert(userAddress, amount, privateKey);
            } catch (error) {
                expect(error.message).to.equal('Conversion transaction failed');
            }
        });
    });

    describe('checkBalance', () => {
        it('should return the user balance', async () => {
            const balance = 200;

            // Mock the method
            mockContract.check Balance.returns(Promise.resolve(balance));

            const result = await conversionService.checkBalance(userAddress);
            expect(result).to.equal(balance);
        });

        it('should throw an error if balance check fails', async () => {
            // Mock the method to throw an error
            mockContract.checkBalance.throws(new Error('Balance check failed'));

            try {
                await conversionService.checkBalance(userAddress);
            } catch (error) {
                expect(error.message).to.equal('Balance check failed');
            }
        });
    });
}); 
