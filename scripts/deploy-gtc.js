const gtc = require('../src/tokens/gtc');
const stability = require('../src/tokens/stability');
const GalacticWallet = require('../src/tokens/wallet');
const BioQuantumIntegrationLayer = require('../src/tokens/bqil');
const gwmp = require('../core/gwmp');
const qtdc = require('../core/qtdc');
const qgc = require('../core/qgc');
const aies = require('../src/space/aies');
const dotenv = require('dotenv');

dotenv.config(); // Load environment variables

async function deployGTC() {
    try {
        console.log("Deploying Galactic Coin (GTC) pegged at $314,159 with subunit Galactic Unit (GU)...");

        // Initialize GTC
        await gtc.initialize();
        console.log("GTC initialized successfully.");

        // Create wallets for users
        const wallet1Address = process.env.WALLET1_ADDRESS || "0xUser 1";
        const wallet2Address = process.env.WALLET2_ADDRESS || "0xUser 2";
        const wallet1 = new GalacticWallet(wallet1Address);
        const wallet2 = new GalacticWallet(wallet2Address);
        console.log(`Wallets created: ${wallet1.address}, ${wallet2.address}`);

        // Simulate adding a valid bio-signal for authentication
        const bioSignal = 'validBioSignal'; // Simulated bio-signal
        await BioQuantumIntegrationLayer.addValidBioSignal(bioSignal);
        console.log("Valid bio-signal added for authentication.");

        // Authenticate using BQIL
        await BioQuantumIntegrationLayer.authenticate(bioSignal);
        console.log("BQIL authentication successful.");

        // Transfer GTC to wallets
        await transferGTC(gtc.owner, wallet1.address, 1000, bioSignal);
        await transferGTC(gtc.owner, wallet2.address, 500, bioSignal);

        // Send Galactic Units (GU) from wallet1 to wallet2
        await sendGU(wallet1, wallet2, 1000);

        // Check balances
        await checkBalances(wallet1, wallet2);

        // Stabilize GTC price
        await stabilizeGTC();

        // Initialize and activate SRNF
        await initializeSRNF();
    } catch (error) {
        console.error("Error during GTC deployment:", error.message);
    }
}

// Function to transfer GTC
async function transferGTC(from, to, amount, bioSignal) {
    try {
        console.log(`Transferring ${amount} GTC to ${to}...`);
        await gtc.transferGTC(from, to, amount, bioSignal);
        console.log(`Successfully transferred ${amount} GTC to ${to}.`);
    } catch (error) {
        console.error(`Failed to transfer ${amount} GTC to ${to}:`, error.message);
    }
}

// Function to send Galactic Units (GU)
async function sendGU(walletFrom, walletTo, amount) {
    try {
        console.log(`Sending ${amount} GU from ${walletFrom.address} to ${walletTo.address}...`);
        await walletFrom.sendGU(walletTo.address, amount);
        console.log(`Successfully sent ${amount} GU from ${walletFrom.address} to ${walletTo.address}.`);
    } catch (error) {
        console.error(`Failed to send ${amount} GU from ${walletFrom.address} to ${walletTo.address}:`, error.message);
    }
}

// Function to check balances
async function checkBalances(wallet1, wallet2) {
    try {
        console.log(`Checking balances...`);
        const balance1 = await wallet1.checkBalance();
        const balance2 = await wallet2.checkBalance();
        console.log(`Balance of ${wallet1.address}: ${balance1.GTC} GTC, ${balance1.GU} GU`);
        console.log(`Balance of ${wallet2.address}: ${balance2.GTC} GTC, ${balance2.GU} GU`);
    } catch (error) {
        console.error("Failed to check balances:", error.message);
    }
}

// Function to stabilize GTC price
async function stabilizeGTC() {
    try {
        const currentPriceGTC = await stability.getCurrentPriceGTC();
        console.log(`Current price of GTC: $${currentPriceGTC.toFixed(2)}`);
        await stability.stabilize(currentPriceGTC);
        console.log("Stabilization process completed.");
    } catch (error) {
        console.error("Failed to stabilize GTC price:", error.message);
    }
}

// Function to initialize and activate SRNF
async function initializeSRNF() {
    try {
        console.log("Initializing Self-Replicating Node Fabricator (SRNF)...");
        await aies.initialize(); // Ensure AIES is initialized
        console.log("AIES initialized successfully.");

        console.log("Activating SRNF...");
        await aies.evolveInfrastructure(); // Start automatic replication via SRNF
        console.log("SRNF is now replicating nodes across the solar system...");
    } catch (error) {
        console.error("Failed to initialize or activate SRNF:", error.message);
    }
}

// Execute the deployment
deployGTC().catch(console.error);
