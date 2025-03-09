import React, { useState } from 'react';
import { validateAmount, validateCurrency } from '../utils/validation';
import { usePayments } from '../hooks/usePayments';
import Notification from './Notification';

const PaymentForm = () => {
    const [amount, setAmount] = useState('');
    const [currency, setCurrency] = useState('USD');
    const { createPayment } = usePayments();
    const [notification, setNotification] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            validateAmount(parseFloat(amount));
            validateCurrency(currency);
            await createPayment(amount, currency);
            setNotification({ type: 'success', message: 'Payment created successfully!' });
        } catch (error) {
            setNotification({ type: 'error', message: error.message });
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount"
                    required
                />
                <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="ETH">ETH</option>
                </select>
                <button type="submit">Pay</button>
            </form>
            {notification && <Notification type={notification.type} message={notification.message} />}
        </div>
    );
};

export default PaymentForm;
