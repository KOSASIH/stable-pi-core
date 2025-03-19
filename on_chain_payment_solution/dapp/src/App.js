import React from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import PaymentForm from './components/PaymentForm';
import TransactionHistory from './components/TransactionHistory';
import { usePayments } from './hooks/usePayments';
import { useWallet } from './hooks/useWallet';

const App = () => {
    const { account, connect } = useWallet();
    const { transactions } = usePayments();

    return (
        <div>
            <Header />
            <main>
                {!account ? (
                    <button onClick={connect}>Connect Wallet</button>
                ) : (
                    <div>
                        <h2>Connected Account: {account}</h2>
                        <PaymentForm />
                        <TransactionHistory transactions={transactions} />
                    </div>
                )}
            </main>
            <Footer />
        </div>
    );
};

export default App;
