import { useState } from 'react';
import { getWeb3Instance } from '../utils/wallet';
import { formatAmount } from '../utils/paymentUtils';
import Logger from '../utils/logger';

export const usePayments = () => {
    const [transactions, setTransactions] = useState([]);

    const createPayment = async (amount, currency) => {
        const web3 = getWeb3Instance();
        try {
            // Call the smart contract to create a payment
            // Example: await paymentProcessor.methods.createPayment(amount, currency).send({ from: account });
            const formattedAmount = formatAmount(amount, currency);
            // Simulate adding a transaction
            setTransactions([...transactions, { amount: formattedAmount, currency, status: 'Pending' }]);
            Logger.log(`Payment of ${formattedAmount} ${currency} created.`);
        } catch (error) {
            Logger.error(`Error creating payment: ${error.message}`);
            throw new Error('Failed to create payment. Please try again.');
        }
    };

    return { createPayment, transactions };
};
