const Web3 = require('web3');
const { abi: TokenIncentiveABI } = require('../build/contracts/TokenIncentive.json');
const { abi: StakingContractABI } = require('../build/contracts/StakingContract.json');
const HDWalletProvider = require('@truffle/hdwallet-provider');
require('dotenv').config();

const provider = new HDWalletProvider(process.env.MNEMONIC, process.env.INFURA_URL);
const web3 = new Web3(provider);

const interactWithContracts = async () => {
    try {
        const accounts = await web3.eth.getAccounts();
        const tokenIncentiveAddress = process.env.TOKEN_INCENTIVE_ADDRESS; // Set this in your .env file
        const stakingContractAddress = process.env.STAKING_CONTRACT_ADDRESS; // Set this in your .env file

        const tokenIncentive = new web3.eth.Contract(TokenIncentiveABI, tokenIncentiveAddress);
        const stakingContract = new web3.eth.Contract(StakingContractABI, stakingContractAddress);

        // Check the balance of the deployer
        const balance = await tokenIncentive.methods.balanceOf(accounts[0]).call();
        console.log(`Balance of account ${accounts[0]}: ${web3.utils.fromWei(balance, 'ether')} ITK`);

        // Stake tokens
        const amountToStake = web3.utils.toWei("100", "ether"); // Amount to stake (100 tokens)
        console.log(`Staking ${amountToStake} tokens...`);
        await tokenIncentive.methods.approve(stakingContractAddress, amountToStake).send({ from: accounts[0] });
        await stakingContract.methods.stake(amountToStake).send({ from: accounts[0] });
        console.log(`Successfully staked ${amountToStake} tokens.`);

        // Check staking balance
        const stakingBalance = await stakingContract.methods.stakingBalance(accounts[0]).call();
        console.log(`Staking balance of account ${accounts[0]}: ${web3.utils.fromWei(stakingBalance, 'ether')} tokens`);

        // Unstake tokens
        console.log(`Unstaking ${amountToStake} tokens...`);
        await stakingContract.methods.unstake().send({ from: accounts[0] });
        console.log(`Successfully unstaked tokens.`);

        // Check final balance
        const finalBalance = await tokenIncentive.methods.balanceOf(accounts[0]).call();
        console.log(`Final balance of account ${accounts[0]}: ${web3.utils.fromWei(finalBalance, 'ether')} ITK`);

    } catch (error) {
        console.error("Error during contract interaction:", error);
    } finally {
        provider.engine.stop(); // Ensure the provider engine is stopped
    }
};

interactWithContracts().catch(console.error);
