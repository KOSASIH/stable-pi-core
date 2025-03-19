import { connectWallet, getWeb3Instance } from './wallet';

export const setupWalletProvider = () => {
    if (window.ethereum) {
        window.ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length === 0) {
                console.log('Please connect to MetaMask.');
            } else {
                console.log('Account changed:', accounts[0]);
                // Optionally, you can update your application state here
                alert(`Account changed to: ${accounts[0]}`);
            }
        });

        window.ethereum.on('chainChanged', (chainId) => {
            console.log('Network changed to:', chainId);
            alert(`Network changed to: ${chainId}`);
            // Optionally, you can reload the page or update your application state here
            window.location.reload();
        });
    } else {
        console.error('No Ethereum provider found. Install MetaMask.');
        alert('No Ethereum provider found. Install MetaMask.');
    }
};

// Call this function to initialize the wallet provider
export const initializeWallet = async () => {
    try {
        await connectWallet();
        setupWalletProvider();
    } catch (error) {
        console.error('Error initializing wallet:', error);
        alert(`Error initializing wallet: ${error.message}`);
    }
};
