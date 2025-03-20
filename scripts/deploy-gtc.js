// scripts/deploy-gtc.js
const gtc = require('../src/tokens/gtc');
const stability = require('../src/tokens/stability');

async function deployGTC() {
  console.log("Deploying Galactic Coin (GTC) pegged at $314,159 with subunit Galactic Unit (GU)...");
  await gtc.initialize();

  const wallet1 = new (require('../src/tokens/wallet'))("0xUser1");
  const wallet2 = new (require('../src/tokens/wallet'))("0xUser2");

  await gtc.transferGTC(gtc.owner, wallet1.address, 1000); // 1000 GTC
  await gtc.transferGTC(gtc.owner, wallet2.address, 500);  // 500 GTC

  await wallet1.sendGU(wallet2.address, 1000); // 1000 GU = $1000
  wallet1.checkBalance();
  wallet2.checkBalance();

  const currentPriceGTC = stability.getCurrentPriceGTC();
  await stability.stabilize(currentPriceGTC);
}

deployGTC().catch(console.error);
