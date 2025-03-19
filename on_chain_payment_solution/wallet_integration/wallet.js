import Web3 from 'web3';

let web3;
let currentAccount = null;

export const connectWallet = async () => {
    if (window.ethereum) {
        try {
            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            currentAccount = accounts[0];
            web3 = new Web3(window.ethereum);
            console.log('Wallet connected:', currentAccount);
            return currentAccount;
        } catch (error) {
            if (error.code === 4001) {
                console.error('User  denied account access');
                throw new Error('User  denied account access');
            } else {
                console.error('Error connecting to wallet:', error);
                throw new Error('Error connecting to wallet');
            }
        }
    } else {
        console.error('No Ethereum provider found. Install MetaMask.');
        throw new Error('No Ethereum provider found. Install MetaMask.');
    }
};

export const getCurrentAccount = () => {
    return currentAccount;
};

export const isWalletConnected = () => {
    return currentAccount !== null;
};

export const disconnectWallet = () => {
    currentAccount = null;
    web3 = null;
    console.log('Wallet disconnected');
};

export const getWeb3Instance = () => {
    if (!web3) {
        throw new Error('Web3 is not initialized. Please connect your wallet first.');
    }
    return web3;
};

// New function to get the balance of the current account
export const getAccountBalance = async () => {
    if (!currentAccount) {
        throw new Error('No account connected');
    }
    const balance = await web3.eth.getBalance(currentAccount);
    return web3.utils.fromWei(balance, 'ether'); // Convert from Wei to Ether
};
