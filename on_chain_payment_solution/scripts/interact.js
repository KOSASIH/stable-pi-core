const Web3 = require('web3');
const PaymentProcessor = require('./build/contracts/PaymentProcessor.json');
const RefundManager = require('./build/contracts/RefundManager.json');

const web3 = new Web3('http://localhost:8545'); // Connect to your Ethereum node

async function main() {
    const accounts = await web3.eth.getAccounts();
    const paymentProcessorInstance = new web3.eth.Contract(PaymentProcessor.abi, 'YOUR_PAYMENT_PROCESSOR_ADDRESS');
    const refundManagerInstance = new web3.eth.Contract(RefundManager.abi, 'YOUR_REFUND_MANAGER_ADDRESS');

    // Example: Create a payment
    const amount = web3.utils.toWei('0.1', 'ether'); // Amount in wei
    const currency = 'USD'; // Example currency
    await paymentProcessorInstance.methods.createPayment(amount, currency).send({ from: accounts[0], value: amount });

    console.log('Payment created successfully.');

    // Example: Request a refund
    const paymentId = 1; // Replace with the actual payment ID
    await refundManagerInstance.methods.requestRefund(paymentId).send({ from: accounts[0] });

    console.log('Refund requested successfully.');

    // Example: Process a refund
    await refundManagerInstance.methods.processRefund(paymentId).send({ from: accounts[0] });

    console.log('Refund processed successfully.');
}

main().catch(console.error);
