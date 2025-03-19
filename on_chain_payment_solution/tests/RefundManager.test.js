const RefundManager = artifacts.require("RefundManager");
const PaymentProcessor = artifacts.require("PaymentProcessor");

contract("RefundManager", (accounts) => {
    let refundManager;
    let paymentProcessor;

    before(async () => {
        paymentProcessor = await PaymentProcessor.new();
        refundManager = await RefundManager.new(paymentProcessor.address);
    });

    it("should request a refund", async () => {
        const amount = web3.utils.toWei('0.1', 'ether');
        const currency = 'USD';

        await paymentProcessor.createPayment(amount, currency, { from: accounts[0], value: amount });
        await paymentProcessor.completePayment(1, { from: accounts[0] });

        const result = await refundManager.requestRefund(1, { from: accounts[0] });
        assert.equal(result.logs[0].event, "RefundRequested", "RefundRequested event should be emitted");
    });

    it("should process a refund", async () => {
        await refundManager.processRefund(1, { from: accounts[0] });
        const payment = await paymentProcessor.getPaymentDetails(1);
        assert.equal(payment.status.toString(), "2", "Payment status should be Refunded");
    });

    it("should deny a refund", async () => {
        const reason = "Refund request denied due to policy.";
        const result = await refundManager.denyRefund(1, reason, { from: accounts[0] });
        assert.equal(result.logs[0].event, "RefundDenied", "RefundDenied event should be emitted");
    });
});
