const gtc = require('../src/tokens/gtc');
const stability = require('../src/tokens/stability');
const GalacticWallet = require('../src/tokens/wallet');
const BioQuantumIntegrationLayer = require('../src/tokens/bqil');
const dotenv = require('dotenv');

dotenv.config(); // Load environment variables

async function deployGTC() {
    try {
        console.log("Deploying Galactic Coin (GTC) pegged at $314,159 with subunit Galactic Unit (GU)...");

        await gtc.initialize();

        const wallet1 = new GalacticWallet(process.env.WALLET1_ADDRESS || "0xUser 1");
        const wallet2 = new GalacticWallet(process.env.WALLET2_ADDRESS || "0xUser 2");

        // Simulate adding a valid bio-signal for authentication
        const bioSignal = 'validBioSignal'; // Simulated bio-signal
        await BioQuantumIntegrationLayer.addValidBioSignal(bioSignal); // Add valid bio-signal for testing

        // Authenticate using BQIL
        await BioQuantumIntegrationLayer.authenticate(bioSignal);
        console.log("BQIL authentication successful.");

        console.log(`Transferring 1000 GTC to ${wallet1.address}...`);
        await gtc.transferGTC(gtc.owner, wallet1.address, 1000, bioSignal); // 1000 GTC
        console.log(`Transferring 500 GTC to ${wallet2.address}...`);
        await gtc.transferGTC(gtc.owner, wallet2.address, 500, bioSignal);  // 500 GTC

        console.log(`Sending 1000 GU from ${wallet1.address} to ${wallet2.address}...`);
        await wallet1.sendGU(wallet2.address, 1000); // 1000 GU = $1000

        console.log(`Checking balances...`);
        const balance1 = await wallet1.checkBalance();
        const balance2 = await wallet2.checkBalance();
        console.log(`Balance of ${wallet1.address}: ${balance1.GTC} GTC, ${balance1.GU} GU`);
        console.log(`Balance of ${wallet2.address}: ${balance2.GTC} GTC, ${balance2.GU} GU`);

        const currentPriceGTC = stability.getCurrentPriceGTC();
        console.log(`Current price of GTC: $${currentPriceGTC.toFixed(2)}`);
        await stability.stabilize(currentPriceGTC);
        console.log("Stabilization process completed.");
    } catch (error) {
        console.error("Error during GTC deployment:", error.message);
    }
}

deployGTC().catch(console.error);
