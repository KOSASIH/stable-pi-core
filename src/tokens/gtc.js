// src/tokens/gtc.js
const { qgc } = require('../core/qgc');
const { tcp } = require('../quantum/tcp');
const { aqps } = require('../quantum/aqps');
const { hql } = require('../core/hql');

class GalacticCoin {
  constructor() {
    this.name = "Galactic Coin";
    this.symbol = "GTC";
    this.subunitName = "Galactic Unit";
    this.subunitSymbol = "GU";
    this.totalSupply = 1000000000; // 1 billion GTC
    this.stableValueGTC = 314159; // 1 GTC = $314,159
    this.subunitRatio = 314159; // 1 GTC = 314,159 GU, 1 GU = $1
    this.balances = new Map(); // Balances in GTC
    this.owner = "0xInitialDeployer"; // Replace with your address
    this.transactionFeePercentage = 0.01; // 1% transaction fee
    this.eventLog = []; // Event log for transactions
  }

  async initialize() {
    this.balances.set(this.owner, this.totalSupply);
    await hql.store("GTC_INITIALIZED", {
      totalSupply: this.totalSupply,
      stableValueGTC: this.stableValueGTC,
      subunitRatio: this.subunitRatio,
      timestamp: Date.now()
    });
    console.log(`${this.name} (${this.symbol}) initialized with ${this.totalSupply} GTC, pegged at $${this.stableValueGTC}. 1 GTC = ${this.subunitRatio} GU`);
  }

  async transferGTC(from, to, amountGTC) {
    const amountGU = amountGTC * this.subunitRatio;
    const fee = amountGTC * this.transactionFeePercentage;
    const netAmountGTC = amountGTC - fee;

    if ((this.balances.get(from) || 0) < amountGTC) throw new Error("Insufficient balance");
    if (netAmountGTC <= 0) throw new Error("Transfer amount must be greater than transaction fee");

    const tx = aqps.encrypt({ from, to, amountGTC, netAmountGTC, fee, amountGU, timestamp: Date.now() });
    await tcp.send(tx);
    const confirmed = await qgc.confirm(tx);
    if (!confirmed) throw new Error("Consensus failed");

    this.balances.set(from, (this.balances.get(from) || 0) - amountGTC);
    this.balances.set(to, (this.balances.get(to) || 0) + netAmountGTC);
    this.balances.set(this.owner, (this.balances.get(this.owner) || 0) + fee); // Fee goes to owner

    await hql.store(`TX_${Date.now()}`, tx);
    this.eventLog.push({ from, to, amountGTC, fee, timestamp: Date.now() });
    console.log(`Transferred ${netAmountGTC} GTC ($${netAmountGTC * this.stableValueGTC}, ${amountGU} GU) from ${from} to ${to} with a fee of ${fee} GTC`);
  }

  async transferGU(from, to, amountGU) {
    const amountGTC = amountGU / this.subunitRatio;
    await this.transferGTC(from, to, amountGTC);
  }

  getBalance(address) {
    const balanceGTC = this.balances.get(address) || 0;
    const balanceGU = balanceGTC * this.subunitRatio;
    return { GTC: balanceGTC, GU: balanceGU };
  }

  getTransactionHistory() {
    return this.eventLog;
  }
}

module.exports = new GalacticCoin();
