// Check if Web3 is injected by the browser (MetaMask)
if (typeof window.ethereum !== 'undefined') {
    console.log('MetaMask is installed!');
} else {
    alert('Please install MetaMask to use this DApp!');
}

// Elements from the DOM
const connectButton = document.getElementById('connectButton');
const disconnectButton = document.getElementById('disconnectButton');
const accountInfo = document.getElementById('accountInfo');
const accountParagraph = document.getElementById('account');

// Connect to the user's wallet
connectButton.addEventListener('click', async () => {
    try {
        // Request account access if needed
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
        const account = accounts[0];

        // Display the account information
        accountParagraph.innerText = account;
        accountInfo.style.display = 'block';
        connectButton.style.display = 'none';
    } catch (error) {
        console.error('User  denied account access or error occurred:', error);
    }
});

// Disconnect the wallet
disconnectButton.addEventListener('click', () => {
    accountInfo.style.display = 'none';
    connectButton.style.display = 'block';
    accountParagraph.innerText = '';
});

// Initialize Web3
let web3;
async function initWeb3() {
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(window.ethereum);
        console.log('Web3 initialized:', web3);
    } else {
        console.error('Web3 is not available. Please install MetaMask.');
    }
}

// Call this function to initialize Web3 and the contract
initWeb3();

// Example function to interact with a smart contract
async function getContractData() {
    const contractAddress = 'YOUR_CONTRACT_ADDRESS'; // Replace with your contract address
    const contractABI = [ /* Your contract ABI here */ ]; // Replace with your contract ABI

    const contract = new web3.eth.Contract(contractABI, contractAddress);

    try {
        const data = await contract.methods.yourMethodName().call(); // Replace with your method name
        console.log('Contract data:', data);
    } catch (error) {
        console.error('Error fetching contract data:', error);
    }
}

// Uncomment to call the function when needed
// getContractData();
