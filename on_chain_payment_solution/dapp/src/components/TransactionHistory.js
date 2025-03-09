import React from 'react';

const TransactionHistory = ({ transactions }) => {
    return (
        <div>
            <h2>Transaction History</h2>
            <ul>
                {transactions.map((tx, index) => (
                    <li key={index}>
                        {tx.amount} {tx.currency} - {tx.status}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TransactionHistory;
