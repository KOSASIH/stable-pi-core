#!/bin/bash

# Deployment script for the smart contracts and API

# Set environment variables
export ETH_NODE="http://127.0.0.1:8545"
export DEPLOYER_ACCOUNT="0xYourDeployerAccountAddress"

# Deploy the Stablecoin contract
echo "Deploying Stablecoin contract..."
brownie run scripts/deploy_stablecoin.py --network development

# Deploy the Governance contract
echo "Deploying Governance contract..."
brownie run scripts/deploy_governance.py --network development

# Start the Flask API
echo "Starting the Flask API..."
cd src/api
flask run &

echo "Deployment completed successfully!"
