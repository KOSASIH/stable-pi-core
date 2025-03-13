// migrations/3_deploy_amm.js
const AMM = artifacts.require("AMM");

module.exports = function (deployer) {
  deployer.deploy(AMM)
    .then(() => {
      console.log("AMM deployed at:", AMM.address);
    });
};
