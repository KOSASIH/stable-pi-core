// migrations/2_deploy_collateral.js
const MultiAssetCollateral = artifacts.require("MultiAssetCollateral");

module.exports = function (deployer) {
  deployer.deploy(MultiAssetCollateral)
    .then(() => {
      console.log("MultiAssetCollateral deployed at:", MultiAssetCollateral.address);
    });
};
