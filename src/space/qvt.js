// src/space/qvt.js
const { starEnergy } = require('../tokens/starEnergy');
const { cnc } = require('../tokens/cnc');
const { tcp } = require('../quantum/tcp');
const EventEmitter = require('events');

class QuantumVortexTransatron extends EventEmitter {
  constructor() {
    super();
    this.active = false;
    this.vortexLocations = new Map();
    this.transactionHistory = [];
  }

  activate() {
    this.active = true;
    console.log("Quantum Vortex Transatron activated.");
    this.initializeVortices();
  }

  initializeVortices() {
    const locations = ['Earth Orbit', 'Mars Surface', 'Proxima Centauri'];
    locations.forEach(loc => this.vortexLocations.set(loc, { active: true }));
    console.log(`Initialized vortices at: ${Array.from(this.vortexLocations.keys()).join(', ')}`);
  }

  addVortex(location) {
    if (this.vortexLocations.has(location)) {
      console.log(`Vortex location ${location} already exists.`);
      return;
    }
    this.vortexLocations.set(location, { active: true });
    console.log(`Added vortex location: ${location}`);
  }

  removeVortex(location) {
    if (!this.vortexLocations.has(location)) {
      console.log(`Vortex location ${location} does not exist.`);
      return;
    }
    this.vortexLocations.delete(location);
    console.log(`Removed vortex location: ${location}`);
  }

  async transportAsset(fromLocation, toLocation, assetType, amount, user) {
    if (!this.vortexLocations.has(fromLocation) || !this.vortexLocations.has(toLocation)) {
      throw new Error("Vortex location not found");
    }
    if (!this.active) throw new Error("QVT not active");

    // Basic authentication check (for demonstration purposes)
    if (!this.authenticateUser(user)) {
      throw new Error("Unauthorized user");
    }

    try {
      const assetTransfer = assetType === 'StarEnergy' ? starEnergy : cnc;
      await assetTransfer.transfer(assetTransfer.owner, 'system-reserve', amount);
      await tcp.send({ event: 'TRANSPORT', asset: assetType, amount, from: fromLocation, to: toLocation });
      
      // Log the transaction
      this.logTransaction(assetType, amount, fromLocation, toLocation);
      
      console.log(`Transported ${amount} ${assetType} from ${fromLocation} to ${toLocation}`);
      this.emit('transportCompleted', { assetType, amount, fromLocation, toLocation });
    } catch (error) {
      console.error(`Error during transport: ${error.message}`);
      throw new Error("Transport failed");
    }
  }

  logTransaction(assetType, amount, fromLocation, toLocation) {
    const transaction = {
      assetType,
      amount,
      fromLocation,
      toLocation,
      timestamp: new Date().toISOString()
    };
    this.transactionHistory.push(transaction);
    console.log(`Transaction logged: ${JSON.stringify(transaction)}`);
  }

  authenticateUser(user) {
    // Placeholder for user authentication logic
    // In a real application, this would check against a user database or authentication service
    return user && user.isAuthenticated;
  }

  deactivate() {
    this.active = false;
    console.log("Quantum Vortex Transatron deactivated.");
  }
}

module.exports = new QuantumVortexTransatron();
