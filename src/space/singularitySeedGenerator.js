// src/space/singularitySeedGenerator.js

const DarkMatterEnergyConverter = require('./darkMatterEnergyConverter'); // Ensure the path is correct

class SingularitySeedGenerator {
    constructor() {
        this.energyOutput = 0; // Energy produced
        this.storageCapacity = 0; // Storage capacity
        this.isActive = false; // Generator status
        this.maxEnergyOutput = 1e12; // Maximum energy output limit
        this.maxStorageCapacity = 1e9; // Maximum storage capacity limit
        this.safetyThreshold = 0.8; // Safety threshold for energy output
        this.dmConverter = new DarkMatterEnergyConverter(); // Initialize the converter
    }

    // Method to activate the generator
    activate() {
        if (!this.isActive) {
            this.isActive = true;
            console.log('Singularity Seed Generator activated.');
            this.generateSingularity();
        } else {
            console.log('Generator is already active.');
        }
    }

    // Method to deactivate the generator
    deactivate() {
        if (this.isActive) {
            this.isActive = false;
            console.log('Singularity Seed Generator deactivated.');
        } else {
            console.log('Generator is already inactive.');
        }
    }

    // Method to generate controlled micro-singularities
    generateSingularity() {
        if (this.isActive) {
            const potentialEnergy = Math.random() * this.maxEnergyOutput; // Random energy output
            const potentialStorage = Math.random() * this.maxStorageCapacity; // Random storage capacity

            // Safety check to ensure energy output is within safe limits
            if (potentialEnergy / this.maxEnergyOutput > this.safetyThreshold) {
                console.warn('Warning: Energy output exceeds safety threshold! Adjusting to safe levels.');
                this.energyOutput = this.maxEnergyOutput * this.safetyThreshold;
            } else {
                this.energyOutput = potentialEnergy;
            }

            this.storageCapacity = potentialStorage;

            console.log(`Generated singularity with energy output: ${this.energyOutput.toFixed(2)} J and storage capacity: ${this.storageCapacity.toFixed(2)} GB.`);

            // If a Dark Matter Energy Converter is set, convert the generated energy
            this.dmConverter.convertEnergy(this.energyOutput);
        } else {
            console.log('Cannot generate singularity. Generator is inactive.');
        }
    }

    // Method to get the generated energy output
    getEnergyOutput() {
        return this.energyOutput;
    }

    // Method to get the storage capacity
    getStorageCapacity() {
        return this.storageCapacity;
    }

    // Method to reset the generator
    reset() {
        this.energyOutput = 0;
        this.storageCapacity = 0;
        console.log('Singularity Seed Generator reset to initial state.');
    }

    // Method to dynamically configure energy output and storage limits
    configure(maxEnergy, maxStorage, safetyThreshold) {
        this.maxEnergyOutput = maxEnergy;
        this.maxStorageCapacity = maxStorage;
        this.safetyThreshold = safetyThreshold;
        console.log(`Configuration updated: Max Energy Output = ${this.maxEnergyOutput}, Max Storage Capacity = ${this.maxStorageCapacity}, Safety Threshold = ${this.safetyThreshold}`);
    }
}

// Export the SSG module
module.exports = SingularitySeedGenerator;
