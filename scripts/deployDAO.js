// scripts/deployDAO.js

const hre = require("hardhat");

async function main() {
    // Deploy the Governance Token
    const GovernanceToken = await hre.ethers.getContractFactory("GovernanceToken");
    const governanceToken = await GovernanceToken.deploy();
    await governanceToken.deployed();
    console.log("Governance Token deployed to:", governanceToken.address);

    // Deploy the Liquidity Pool
    const LiquidityPool = await hre.ethers.getContractFactory("LiquidityPool");
    const liquidityPool = await LiquidityPool.deploy(governanceToken.address);
    await liquidityPool.deployed();
    console.log("Liquidity Pool deployed to:", liquidityPool.address);

    // Deploy the Liquidity Pool DAO
    const LiquidityPoolDAO = await hre.ethers.getContractFactory("LiquidityPoolDAO");
    const liquidityPoolDAO = await LiquidityPoolDAO.deploy(governanceToken.address, liquidityPool.address);
    await liquidityPoolDAO.deployed();
    console.log("Liquidity Pool DAO deployed to:", liquidityPoolDAO.address);
}

// Execute the deployment script
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
