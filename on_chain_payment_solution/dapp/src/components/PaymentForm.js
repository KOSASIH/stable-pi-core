import React, { useState } from 'react';
import { validateAmount, validateCurrency } from '../utils/validation';
import { usePayments } from '../hooks/usePayments';
import Notification from './Notification';
import { SUPPORTED_CURRENCIES } from '../utils/constants';

const PaymentForm = () => {
    const [amount, setAmount] = useState('');
    const [currency, setCurrency] = useState(SUPPORTED_CURRENCIES[0]); // Default to the first currency
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
                    {SUPPORTED_CURRENCIES.map((curr) => (
                        <option key={curr} value={curr}>{curr}</option>
                    ))}
                </select>
                <button type="submit">Pay</button>
            </form>
            {notification && <Notification type={notification.type} message={notification.message} />}
        </div>
    );
};

export default PaymentForm;
