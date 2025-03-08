const Web3 = require('web3');
const { abi: TokenIncentiveABI, evm: { bytecode: TokenIncentiveBytecode } } = require('../build/contracts/TokenIncentive.json');
const { abi: StakingContractABI, evm: { bytecode: StakingContractBytecode } } = require('../build/contracts/StakingContract.json');
const HDWalletProvider = require('@truffle/hdwallet-provider');
require('dotenv').config();

const provider = new HDWalletProvider(process.env.MNEMONIC, process.env.INFURA_URL);
const web3 = new Web3(provider);

const deployContracts = async () => {
    try {
        const accounts = await web3.eth.getAccounts();
        console.log("Deploying contracts from account:", accounts[0]);

        // Deploy TokenIncentive contract
        const tokenIncentive = await new web3.eth.Contract(TokenIncentiveABI)
            .deploy({ data: TokenIncentiveBytecode })
            .send({ from: accounts[0], gas: '3000000' });

        console.log("TokenIncentive deployed at:", tokenIncentive.options.address);

        // Define initial reward rate for StakingContract
        const initialRewardRate = web3.utils.toWei("1", "ether"); // 1 token per second

        // Deploy StakingContract
        const stakingContract = await new web3.eth.Contract(StakingContractABI)
            .deploy({ data: StakingContractBytecode, arguments: [tokenIncentive.options.address, initialRewardRate] })
            .send({ from: accounts[0], gas: '3000000' });

        console.log("StakingContract deployed at:", stakingContract.options.address);

        // Mint initial tokens to the deployer
        const initialSupply = web3.utils.toWei("1000000", "ether"); // 1 million tokens
        await tokenIncentive.methods.mint(accounts[0], initialSupply).send({ from: accounts[0] });
        console.log(`Minted ${initialSupply} tokens to account: ${accounts[0]}`);

        // Set the initial reward rate
        await tokenIncentive.methods.setRewardRate(initialRewardRate).send({ from: accounts[0] });
        console.log(`Initial reward rate set to: ${initialRewardRate} tokens per second`);

    } catch (error) {
        console.error("Error during contract deployment:", error);
        throw error; // Rethrow the error to stop the deployment process
    } finally {
        provider.engine.stop(); // Ensure the provider engine is stopped
    }
};

deployContracts().catch(console.error);
