// Ensure Web3 is initialized
if (typeof window.ethereum === 'undefined') {
    console.error('Web3 is not available. Please install MetaMask.');
}

// Replace with your contract address and ABI
const contractAddress = 'YOUR_CONTRACT_ADDRESS'; // Replace with your actual contract address
const contractABI = [
    // Replace with your actual contract ABI
    {
        "constant": true,
        "inputs": [],
        "name": "yourMethodName",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "setValue",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
];

// Initialize Web3 and the contract
let web3;
let contract;

async function initContract() {
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(window.ethereum);
        contract = new web3.eth.Contract(contractABI, contractAddress);
        console.log('Contract initialized:', contract);
    } else {
        console.error('Web3 is not available. Please install MetaMask.');
    }
}

// Call this function to initialize the contract
initContract();

// Function to get data from the contract
async function getData() {
    try {
        const data = await contract.methods.yourMethodName().call(); // Replace with your method name
        console.log('Data from contract:', data);
        return data;
    } catch (error) {
        console.error('Error fetching data from contract:', error);
    }
}

// Function to send a transaction to the contract
async function setData(value) {
    const accounts = await window.ethereum.request({ method: 'eth_accounts' });
    const account = accounts[0];

    try {
        const tx = await contract.methods.setValue(value).send({ from: account });
        console.log('Transaction successful:', tx);
    } catch (error) {
        console.error('Error sending transaction:', error);
    }
}

// Example usage
// Uncomment to call the function when needed
// getData();
// setData(42); // Example to set a value
