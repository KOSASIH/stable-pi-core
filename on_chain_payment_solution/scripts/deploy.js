const Migrations = artifacts.require("Migrations");
const PaymentProcessor = artifacts.require("PaymentProcessor");
const RefundManager = artifacts.require("RefundManager");

module.exports = async function (deployer) {
    // Deploy the Migrations contract first
    await deployer.deploy(Migrations);
    
    // Deploy the PaymentProcessor contract
    await deployer.deploy(PaymentProcessor);
    
    // Get the address of the deployed PaymentProcessor contract
    const paymentProcessorInstance = await PaymentProcessor.deployed();
    
    // Deploy the RefundManager contract with the address of PaymentProcessor
    await deployer.deploy(RefundManager, paymentProcessorInstance.address);
};
