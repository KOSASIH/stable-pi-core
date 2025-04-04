// src/tokens/starEnergy.js

const { Logger } = require('../core/logger'); // Assuming a logger module exists
const CosmicNexusCoin = require('./cnc'); // Import the CNC module

class StarEnergy {
    constructor() {
        this.balance = 0; // Stock of Star Energy
        this.logger = new Logger(); // Initialize logger
        this.valuePerStarEnergy = 1000000; // Value of 1 Star Energy in USD
        this.cncConversionRate = 0.1; // 1 CNC = 0.1 Star Energy
    }

    // Method to harvest Star Energy
    async harvestStarEnergy(amount) {
        try {
            if (amount <= 0) {
                throw new Error("Amount must be positive.");
            }
            this.balance += amount;
            this.logger.info(`Successfully harvested Star Energy: ${amount}`);
            return this.balance; // Return updated balance
        } catch (error) {
            this.logger.error(`Failed to harvest Star Energy: ${error.message}`);
            throw error; // Rethrow error for further handling
        }
    }

    // Method to convert Star Energy to CNC
    async convertStarEnergyToCNC(amount) {
        try {
            if (amount <= 0 || amount > this.balance) {
                throw new Error("Invalid amount for conversion.");
            }
            const cncAmount = amount * this.cncConversionRate; // 1 Star Energy = 0.1 CNC
            this.balance -= amount;
            await CosmicNexusCoin.addCNC(cncAmount); // Assuming addCNC method exists in CNC module
            this.logger.info(`Successfully converted Star Energy to CNC: ${cncAmount}`);
            return cncAmount; // Return amount of CNC generated
        } catch (error) {
            this.logger.error(`Failed to convert Star Energy to CNC: ${error.message}`);
            throw error; // Rethrow error for further handling
        }
    }

    // Method to get balance of Star Energy
    getBalance() {
        return this.balance;
    }

    // Method to get the monetary value of the Star Energy balance
    getMonetaryValue() {
        return this.balance * this.valuePerStarEnergy; // Calculate total value in USD
    }

    // Method to transfer Star Energy to another entity
    async transferStarEnergy(toEntity, amount) {
        try {
            if (amount <= 0 || amount > this.balance) {
                throw new Error("Invalid transfer amount.");
            }
            this.balance -= amount;
            await toEntity.receiveStarEnergy(amount); // Assuming the receiving entity has a receiveStarEnergy method
            this.logger.info(`Transferred ${amount} Star Energy to ${toEntity.id}`);
        } catch (error) {
            this.logger.error(`Failed to transfer Star Energy: ${error.message}`);
            throw error; // Rethrow error for further handling
        }
    }

    // Method to receive Star Energy (for entities that can receive it)
    async receiveStarEnergy(amount) {
        try {
            if (amount <= 0) {
                throw new Error("Amount must be positive.");
            }
            this.balance += amount;
            this.logger.info(`Received ${amount} Star Energy.`);
        } catch (error) {
            this.logger.error(`Failed to receive Star Energy: ${error.message}`);
            throw error; // Rethrow error for further handling
        }
    }
}

module.exports = new StarEnergy();
