// src/tokens/wallet.js
const gtc = require('./gtc');
const EventEmitter = require('events');
const dotenv = require('dotenv');

dotenv.config(); // Load environment variables

class GalacticWallet extends EventEmitter {
  constructor(address) {
    super();
    this.address = address;
    this.transactionHistory = [];
  }

  async sendGTC(to, amountGTC) {
    try {
      const balance = await gtc.getBalance(this.address);
      if (balance.GTC < amountGTC) {
        throw new Error(`Insufficient GTC balance: ${balance.GTC} GTC available.`);
      }

      await gtc.transferGTC(this.address, to, amountGTC);
      const transaction = {
        type: 'GTC',
        to,
        amount: amountGTC,
        timestamp: new Date(),
      };
      this.transactionHistory.push(transaction);
      this.emit('transaction', transaction); // Emit transaction event

      console.log(`Wallet ${this.address} sent ${amountGTC} GTC ($${amountGTC * gtc.stableValueGTC}) to ${to}`);
    } catch (error) {
      console.error(`Error sending GTC: ${error.message}`);
    }
  }

  async sendGU(to, amountGU) {
    try {
      const balance = await gtc.getBalance(this.address);
      if (balance.GU < amountGU) {
        throw new Error(`Insufficient GU balance: ${balance.GU} GU available.`);
      }

      await gtc.transferGU(this.address, to, amountGU);
      const transaction = {
        type: 'GU',
        to,
        amount: amountGU,
        timestamp: new Date(),
      };
      this.transactionHistory.push(transaction);
      this.emit('transaction', transaction); // Emit transaction event

      console.log(`Wallet ${this.address} sent ${amountGU} GU ($${amountGU}) to ${to}`);
    } catch (error) {
      console.error(`Error sending GU: ${error.message}`);
    }
  }

  async checkBalance() {
    try {
      const balance = await gtc.getBalance(this.address);
      console.log(`Balance of ${this.address}: ${balance.GTC} GTC ($${balance.GTC * gtc.stableValueGTC}), ${balance.GU} GU ($${balance.GU})`);
      return balance;
    } catch (error) {
      console.error(`Error checking balance: ${error.message}`);
    }
  }

  getTransactionHistory() {
    return this.transactionHistory;
  }
}

module.exports = GalacticWallet;
