// migrations/4_deploy_token_manager.js
const TokenManager = artifacts.require("TokenManager");

module.exports = function (deployer) {
  deployer.deploy(TokenManager)
    .then((instance) => {
      console.log("TokenManager deployed at:", instance.address);
    })
    .catch((error) => {
      console.error("Error deploying TokenManager:", error);
    });
};
