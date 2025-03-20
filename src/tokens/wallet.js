// src/tokens/wallet.js
const gtc = require('./gtc');

class GalacticWallet {
  constructor(address) {
    this.address = address;
  }

  async sendGTC(to, amountGTC) {
    await gtc.transferGTC(this.address, to, amountGTC);
    console.log(`Wallet ${this.address} sent ${amountGTC} GTC ($${amountGTC * gtc.stableValueGTC}) to ${to}`);
  }

  async sendGU(to, amountGU) {
    await gtc.transferGU(this.address, to, amountGU);
    console.log(`Wallet ${this.address} sent ${amountGU} GU ($${amountGU}) to ${to}`);
  }

  checkBalance() {
    const balance = gtc.getBalance(this.address);
    console.log(`Balance of ${this.address}: ${balance.GTC} GTC ($${balance.GTC * gtc.stableValueGTC}), ${balance.GU} GU ($${balance.GU})`);
    return balance;
  }
}

module.exports = GalacticWallet;
