const PaymentProcessor = artifacts.require("PaymentProcessor");
const RefundManager = artifacts.require("RefundManager");

contract("PaymentProcessor", (accounts) => {
    let paymentProcessor;
    let refundManager;

    before(async () => {
        paymentProcessor = await PaymentProcessor.deployed();
        refundManager = await RefundManager.deployed(paymentProcessor.address);
    });

    it("should create a payment", async () => {
        const amount = web3.utils.toWei('0.1', 'ether');
        const currency = 'USD';

        const result = await paymentProcessor.createPayment(amount, currency, { from: accounts[0], value: amount });
        assert.equal(result.logs[0].event, "PaymentCreated", "PaymentCreated event should be emitted");
    });

    it("should request a refund", async () => {
        const paymentId = 1; // Assuming this payment ID exists

        await refundManager.requestRefund(paymentId, { from: accounts[0] });
        const result = await refundManager.getPaymentDetails(paymentId);
        assert.equal(result.status, 0, "Payment status should be Pending");
    });

    it("should process a refund", async () => {
        const paymentId = 1; // Assuming this payment ID exists

        await refundManager.processRefund(paymentId, { from: accounts[0] });
        const result = await refundManager.getPaymentDetails(paymentId);
        assert.equal(result.status, 2, "Payment status should be Refunded");
    });
});
