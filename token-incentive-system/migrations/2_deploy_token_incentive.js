const TokenIncentive = artifacts.require("TokenIncentive");

module.exports = async function (deployer, network, accounts) {
  try {
    // Define the initial reward rate (in tokens per second)
    const initialRewardRate = web3.utils.toWei("1", "ether"); // 1 token per second

    // Deploy the TokenIncentive contract
    await deployer.deploy(TokenIncentive, { from: accounts[0] });
    console.log("TokenIncentive contract deployed successfully.");

    // Get the deployed instance of the TokenIncentive contract
    const tokenIncentiveInstance = await TokenIncentive.deployed();

    // Optionally, mint initial tokens to the deployer
    const initialSupply = web3.utils.toWei("1000000", "ether"); // 1 million tokens
    await tokenIncentiveInstance.mint(accounts[0], initialSupply);
    console.log(`Minted ${initialSupply} tokens to account: ${accounts[0]}`);

    // Set the initial reward rate
    await tokenIncentiveInstance.setRewardRate(initialRewardRate);
    console.log(`Initial reward rate set to: ${initialRewardRate} tokens per second`);

  } catch (error) {
    console.error("Error during TokenIncentive migration:", error);
    throw error; // Rethrow the error to stop the migration process
  }
};
