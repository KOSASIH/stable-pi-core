// src/space/qnha.js
class QuantumNebulaHarvestingArray {
  constructor() {
    this.energyHarvested = 0; // Total energy harvested
    this.nebulaData = {}; // Store data for each nebula
  }

  // Initialize nebula data with potential energy values
  initializeNebula(nebula, potentialEnergy) {
    this.nebulaData[nebula] = {
      potentialEnergy: potentialEnergy, // Maximum energy that can be harvested
      harvestedEnergy: 0, // Energy already harvested from this nebula
    };
    console.log(`Initialized ${nebula} with potential energy: ${potentialEnergy}`);
  }

  // Harvest energy from a specified nebula
  async harvestFromNebula(nebula) {
    if (!this.nebulaData[nebula]) {
      throw new Error(`Nebula ${nebula} not initialized.`);
    }

    const { potentialEnergy, harvestedEnergy } = this.nebulaData[nebula];
    const remainingEnergy = potentialEnergy - harvestedEnergy;

    if (remainingEnergy <= 0) {
      console.log(`No remaining energy to harvest from ${nebula}.`);
      return 0;
    }

    // Simulate dynamic energy harvesting based on remaining energy
    const energy = Math.min(0.5, remainingEnergy); // Harvest up to 0.5 Star Energy or remaining energy
    this.energyHarvested += energy;
    this.nebulaData[nebula].harvestedEnergy += energy;

    console.log(`Harvested ${energy} Star Energy from ${nebula}. Total harvested: ${this.energyHarvested}`);
    return energy;
  }

  // Convert harvested energy to CNC
  async convertToCNC(energy) {
    if (energy <= 0) {
      throw new Error("Energy must be greater than zero for conversion.");
    }

    const cnc = energy * 10; // 1 Energi Bintang = 10 CNC
    console.log(`Converted ${energy} Star Energy to ${cnc} CNC.`);
    return cnc;
  }

  // Automated harvesting and conversion process
  async automatedHarvestAndConvert(nebula) {
    const energy = await this.harvestFromNebula(nebula);
    if (energy > 0) {
      const cnc = await this.convertToCNC(energy);
      console.log(`Successfully harvested and converted ${energy} Star Energy to ${cnc} CNC.`);
      return cnc;
    }
    return 0;
  }

  // Get total energy harvested
  getTotalEnergyHarvested() {
    return this.energyHarvested;
  }

  // Get energy harvested from a specific nebula
  getNebulaHarvestedEnergy(nebula) {
    if (!this.nebulaData[nebula]) {
      throw new Error(`Nebula ${nebula} not initialized.`);
    }
    return this.nebulaData[nebula].harvestedEnergy;
  }
}

module.exports = new QuantumNebulaHarvestingArray();
