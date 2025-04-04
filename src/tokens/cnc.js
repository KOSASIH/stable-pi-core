// src/tokens/cnc.js
const GalacticWallet = require('./wallet');
const EventEmitter = require('events');

class CosmicNexusCoin extends EventEmitter {
  constructor() {
    super();
    this.owner = 'spc-KOSASIH-owner'; // Your address as the creator
    this.balances = new Map();
    this.balances.set(this.owner, { CNC: 500000 }); // Initial supply of 500,000 CNC
    this.totalSupplyCNC = 500000;
    this.valuePerCNC = 0.1; // Updated: 1 CNC = 0.1 Star Energy
    this.transactionHistory = []; // To keep track of transactions
  }

  async initialize() {
    console.log(`Cosmic Nexus Coin initialized. Owner: ${this.owner}`);
    this.emit('initialized', this.owner);
  }

  async transferCNC(from, to, amount) {
    this.validateAddress(from);
    this.validateAddress(to);
    this.validateAmount(amount);

    if (!this.balances.has(from)) throw new Error("Sender not found");
    if (this.balances.get(from).CNC < amount) throw new Error("Insufficient CNC");

    if (!this.balances.has(to)) this.balances.set(to, { CNC: 0 });

    // Perform the transfer
    this.balances.get(from).CNC -= amount;
    this.balances.get(to).CNC += amount;

    // Log the transaction
    this.logTransaction(from, to, amount);
    console.log(`Transferred ${amount} CNC from ${from} to ${to}`);
    this.emit('transfer', { from, to, amount });
  }

  checkBalance(address) {
    this.validateAddress(address);
    return this.balances.get(address) || { CNC: 0 };
  }

  logTransaction(from, to, amount) {
    const transaction = {
      from,
      to,
      amount,
      timestamp: new Date().toISOString(),
    };
    this.transactionHistory.push(transaction);
    console.log(`Transaction logged: ${JSON.stringify(transaction)}`);
  }

  validateAddress(address) {
    if (typeof address !== 'string' || address.length === 0) {
      throw new Error("Invalid address");
    }
  }

  validateAmount(amount) {
    if (typeof amount !== 'number' || amount <= 0) {
      throw new Error("Invalid amount");
    }
  }

  getTransactionHistory() {
    return this.transactionHistory;
  }

  async mintCNC(to, amount) {
    this.validateAddress(to);
    this.validateAmount(amount);

    if (!this.balances.has(to)) this.balances.set(to, { CNC: 0 });
    this.balances.get(to).CNC += amount;
    this.totalSupplyCNC += amount;

    console.log(`Minted ${amount} CNC to ${to}`);
    this.emit('mint', { to, amount });
  }

  async burnCNC(from, amount) {
    this.validateAddress(from);
    this.validateAmount(amount);

    if (!this.balances.has(from)) throw new Error("Sender not found");
    if (this.balances.get(from).CNC < amount) throw new Error("Insufficient CNC");

    this.balances.get(from).CNC -= amount;
    this.totalSupplyCNC -= amount;

    console.log(`Burned ${amount} CNC from ${from}`);
    this.emit('burn', { from, amount });
  }
}

module.exports = new CosmicNexusCoin();
