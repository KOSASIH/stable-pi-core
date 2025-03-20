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
    this.totalSupply = 1000000000; // 1 miliar GTC
    this.stableValueGTC = 314159; // 1 GTC = $314,159
    this.subunitRatio = 314159; // 1 GTC = 314,159 GU, 1 GU = $1
    this.balances = new Map(); // Saldo dalam GTC
    this.owner = "0xInitialDeployer"; // Ganti dengan alamat Anda
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
    if ((this.balances.get(from) || 0) * this.subunitRatio < amountGU) throw new Error("Insufficient balance");

    const tx = aqps.encrypt({ from, to, amountGTC, amountGU, timestamp: Date.now() });
    await tcp.send(tx);
    const confirmed = await qgc.confirm(tx);
    if (!confirmed) throw new Error("Consensus failed");

    this.balances.set(from, (this.balances.get(from) || 0) - amountGTC);
    this.balances.set(to, (this.balances.get(to) || 0) + amountGTC);
    await hql.store(`TX_${Date.now()}`, tx);
    console.log(`Transferred ${amountGTC} GTC ($${amountGTC * this.stableValueGTC}, ${amountGU} GU) from ${from} to ${to}`);
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
}

module.exports = new GalacticCoin();
