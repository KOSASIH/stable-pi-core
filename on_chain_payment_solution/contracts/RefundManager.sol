// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./PaymentProcessor.sol"; // Import the PaymentProcessor contract

contract RefundManager is Ownable {
    using SafeMath for uint256;

    PaymentProcessor public paymentProcessor;

    event RefundRequested(uint256 indexed paymentId, address indexed requester);
    event RefundProcessed(uint256 indexed paymentId, address indexed payer, uint256 amount);

    constructor(address _paymentProcessorAddress) {
        paymentProcessor = PaymentProcessor(_paymentProcessorAddress);
    }

    function requestRefund(uint256 _paymentId) external {
        PaymentProcessor.Payment memory payment = paymentProcessor.getPaymentDetails(_paymentId);
        require(payment.id != 0, "Payment does not exist");
        require(payment.payer == msg.sender, "Only the payer can request a refund");
        require(payment.status == PaymentProcessor.PaymentStatus.Pending, "Payment is not eligible for refund");

        emit RefundRequested(_paymentId, msg.sender);
    }

    function processRefund(uint256 _paymentId) external onlyOwner {
        PaymentProcessor.Payment memory payment = paymentProcessor.getPaymentDetails(_paymentId);
        require(payment.id != 0, "Payment does not exist");
        require(payment.status == PaymentProcessor.PaymentStatus.Pending, "Payment is not eligible for refund");

        paymentProcessor.refundPayment(_paymentId); // Call the refund function in PaymentProcessor
        emit RefundProcessed(_paymentId, payment.payer, payment.amount);
    }
}
