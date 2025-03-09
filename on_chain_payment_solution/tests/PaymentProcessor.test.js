const PaymentProcessor = artifacts.require("PaymentProcessor");

contract("PaymentProcessor", (accounts) => {
    let paymentProcessor;

    before(async () => {
        paymentProcessor = await PaymentProcessor.deployed();
    });

    it("should create a payment", async () => {
        const amount = web3.utils.toWei('0.1', 'ether');
        const currency = 'USD';

        const result = await paymentProcessor.createPayment(amount, currency, { from: accounts[0], value: amount });
        assert.equal(result.logs[0].event, "PaymentCreated", "PaymentCreated event should be emitted");

        const payment = await paymentProcessor.getPaymentDetails(1);
        assert.equal(payment.amount.toString(), amount, "Payment amount should match");
        assert.equal(payment.currency, currency, "Payment currency should match");
        assert.equal(payment.status.toString(), "0", "Payment status should be Pending");
    });

    it("should complete a payment", async () => {
        await paymentProcessor.completePayment(1, { from: accounts[0] });
        const payment = await paymentProcessor.getPaymentDetails(1);
        assert.equal(payment.status.toString(), "1", "Payment status should be Completed");
    });

    it("should refund a payment", async () => {
        await paymentProcessor.createPayment(web3.utils.toWei('0.1', 'ether'), 'USD', { from: accounts[0], value: web3.utils.toWei('0.1', 'ether') });
        await paymentProcessor.completePayment(2, { from: accounts[0] });

        const payment = await paymentProcessor.getPaymentDetails(2);
assert.equal(payment.status.toString(), "1", "Payment status should be Completed");

        await paymentProcessor.refundPayment(2, { from: accounts[0] });
        const refundedPayment = await paymentProcessor.getPaymentDetails(2);
        assert.equal(refundedPayment.status.toString(), "2", "Payment status should be Refunded");
    });
});
