// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PaymentProcessor is Ownable {
    using SafeMath for uint256;

    enum PaymentStatus { Pending, Completed, Refunded }

    struct Payment {
        uint256 id;
        address payer;
        uint256 amount;
        string currency;
        PaymentStatus status;
        uint256 createdAt;
    }

    mapping(uint256 => Payment) public payments;
    uint256 public paymentCount;

    event PaymentCreated(uint256 indexed paymentId, address indexed payer, uint256 amount, string currency);
    event PaymentCompleted(uint256 indexed paymentId);
    event PaymentRefunded(uint256 indexed paymentId);

    constructor() {
        paymentCount = 0;
    }

    function createPayment(uint256 _amount, string memory _currency) external payable {
        require(_amount > 0, "Amount must be greater than zero");
        require(msg.value == _amount, "Incorrect Ether value sent");

        paymentCount = paymentCount.add(1);
        payments[paymentCount] = Payment({
            id: paymentCount,
            payer: msg.sender,
            amount: _amount,
            currency: _currency,
            status: PaymentStatus.Pending,
            createdAt: block.timestamp
        });

        emit PaymentCreated(paymentCount, msg.sender, _amount, _currency);
    }

    function completePayment(uint256 _paymentId) external onlyOwner {
        Payment storage payment = payments[_paymentId];
        require(payment.id != 0, "Payment does not exist");
        require(payment.status == PaymentStatus.Pending, "Payment already completed or refunded");

        payment.status = PaymentStatus.Completed;
        emit PaymentCompleted(_paymentId);
    }

    function refundPayment(uint256 _paymentId) external onlyOwner {
        Payment storage payment = payments[_paymentId];
        require(payment.id != 0, "Payment does not exist");
        require(payment.status == PaymentStatus.Pending, "Payment already completed or refunded");

        payment.status = PaymentStatus.Refunded;
        payable(payment.payer).transfer(payment.amount); // Refund the payer
        emit PaymentRefunded(_paymentId);
    }

    function getPaymentDetails(uint256 _paymentId) external view returns (Payment memory) {
        return payments[_paymentId];
    }
}
