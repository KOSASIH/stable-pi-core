const StakingContract = artifacts.require("StakingContract");
const TokenIncentive = artifacts.require("TokenIncentive");

module.exports = async function (deployer, network, accounts) {
  try {
    // Get the deployed instance of the TokenIncentive contract
    const tokenIncentiveInstance = await TokenIncentive.deployed();

    // Define the initial reward rate for staking (in tokens per second)
    const stakingRewardRate = web3.utils.toWei("0.5", "ether"); // 0.5 tokens per second

    // Deploy the StakingContract, linking it to the TokenIncentive contract
    await deployer.deploy(StakingContract, tokenIncentiveInstance.address, stakingRewardRate);
    console.log("StakingContract deployed successfully.");

    // Get the deployed instance of the StakingContract
    const stakingContractInstance = await StakingContract.deployed();

    // Optionally, you can set up any initial state or configurations here
    // For example, you could initialize any parameters or mint tokens if needed

    console.log(`StakingContract linked to TokenIncentive at address: ${tokenIncentiveInstance.address}`);
    console.log(`Initial staking reward rate set to: ${stakingRewardRate} tokens per second`);

  } catch (error) {
    console.error("Error during StakingContract migration:", error);
    throw error; // Rethrow the error to stop the migration process
  }
};
