const PaymentProcessor = artifacts.require("PaymentProcessor");
const RefundManager = artifacts.require("RefundManager");

contract("DApp Integration Tests", (accounts) => {
    let paymentProcessor;
    let refundManager;

    before(async () => {
        paymentProcessor = await PaymentProcessor.new();
        refundManager = await RefundManager.new(paymentProcessor.address);
    });

    it("should create a payment and request a refund", async () => {
        const amount = web3.utils.toWei('0.1', 'ether');
        const currency = 'USD';

        // Create a payment
        await paymentProcessor.createPayment(amount, currency, { from: accounts[0], value: amount });
        const payment = await paymentProcessor.getPaymentDetails(1);
        assert.equal(payment.status.toString(), "0", "Payment status should be Pending");

        // Request a refund
        await refundManager.requestRefund(1, { from: accounts[0] });
        const refundRequest = await refundManager.getPaymentDetails(1);
        assert.equal(refundRequest.status.toString(), "0", "Refund request should be Pending");
    });

    it("should process a refund after request", async () => {
        // Complete the payment
        await paymentProcessor.completePayment(1, { from: accounts[0] });

        // Process the refund
        await refundManager.processRefund(1, { from: accounts[0] });
        const payment = await paymentProcessor.getPaymentDetails(1);
        assert.equal(payment.status.toString(), "2", "Payment status should be Refunded");
    });
});
