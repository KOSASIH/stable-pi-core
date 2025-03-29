import TemporalTransactionRewind from './ttr';
import AccessControl from './accessControl';
import Transaction from './transaction';
import { generateQuantumHash, validateQuantumSignature } from './utils';
import SEBD from './sebd'; // Import the Self-Evolving Blockchain DNA module
import DimensionalCompressionEngine from './dce'; // Import the Dimensional Compression Engine
import GalacticEntropyReversalSystem from './gers'; // Import the Galactic Entropy Reversal System
import CSRFProtection from './csrf_layer'; // Import CSRF Protection
import InfiniteHorizonDataVortex from './ihdv'; // Import the Infinite Horizon Data Vortex
import EternalResonanceContinuityField from './ercf'; // Import the ERCF
import CosmicMemoryImprintNetwork from './cmin'; // Import the Cosmic Memory Imprint Network

class HolographicQuantumLedger {
    constructor() {
        this.transactions = [];
        this.ttr = new TemporalTransactionRewind(this);
        this.accessControl = new AccessControl();
        this.ces = new CosmicEntropyShield(); // Integrate Cosmic Entropy Shield
        this.sebd = new SEBD(); // Ensure SEBD is instantiated
        this.dce = new DimensionalCompressionEngine(); // Ensure DCE is instantiated
        this.gers = new GalacticEntropyReversalSystem(); // Ensure GERS is instantiated
        this.csrfProtection = new CSRFProtection(); // Initialize CSRF Protection
        this.ihdv = new InfiniteHorizonDataVortex(); // Instantiate IHDV
        this.erfc = new EternalResonanceContinuityField(); // Integrate ERCF
        this.cmin = new CosmicMemoryImprintNetwork(); // Instantiate CMIN
    }

    initializeHQL(darkMatterEnergyConverter) {
        this.gers.initializeGERS(darkMatterEnergyConverter);
        this.erfc.activate(); // Activate the ERCF during initialization
        console.log("Holographic Quantum Ledger initialized with Galactic Entropy Reversal System and ERCF.");
    }

    createTransaction(data, user, csrfToken) {
        if (!this.accessControl.isAuthorized(user)) {
            throw new Error("Unauthorized access to create transaction.");
        }
        this.csrfProtection.verify_token(user.id, csrfToken); // CSRF check

        const protectedData = this.ces.protectData(data); // Protect data with CES
        const reversedData = this.gers.reverseEntropy(protectedData); // Reverse entropy on protected data
        const transaction = new Transaction(reversedData);
        transaction.hash = this.generateTransactionHash(transaction);
        
        // Compress and store the transaction data using DCE
        this.dce.compressData(transaction.id, reversedData);

        // Add transaction data to IHDV
        this.ihdv.addData(Date.now(), transaction);

        // Capture memory imprint for the transaction
        this.cmin.captureMemoryImprint({ transactionId: transaction.id, data: reversedData }, user.id, csrfToken);

        this.transactions.push(transaction);
        console.log(`Transaction created: ${transaction.id}`);

        // Integrate with SEBD
        this.sebd.integrateWithLedger();

        return transaction;
    }

    getTransaction(transactionId) {
        const entry = this.transactions.find(tx => tx.id === transactionId);
        if (entry) {
            const data = this.ces.degradeData(entry.data); // Check data integrity
            if (data === null) {
                throw new Error("Data integrity compromised. Unable to retrieve transaction.");
            }
            return { ...entry, data }; // Return transaction with protected data
        }
        throw new Error("Transaction not found.");
    }

    updateTransaction(updatedTransaction, csrfToken) {
        const index = this.transactions.findIndex(tx => tx.id === updatedTransaction.id);
        if (index === -1) {
            throw new Error("Transaction not found.");
        }
        this.csrfProtection.verify_token(updatedTransaction.userId, csrfToken); // CSRF check
        this.transactions[index] = updated Transaction;
        console.log(`Transaction updated: ${updatedTransaction.id}`);
        
        // Capture memory imprint for the updated transaction
        this.cmin.captureMemoryImprint({ transactionId: updatedTransaction.id, data: updatedTransaction.data }, updatedTransaction.userId, csrfToken);
    }

    rewindTransaction(transactionId, targetTimestamp, user, csrfToken) {
        this.csrfProtection.verify_token(user.id, csrfToken); // CSRF check
        return this.ttr.rewindTransaction(transactionId, targetTimestamp, user);
    }

    generateTransactionHash(transaction) {
        return generateQuantumHash(transaction);
    }

    validateTransactionSignature(transaction) {
        return validateQuantumSignature(transaction);
    }

    getAllTransactions() {
        return this.transactions;
    }

    clearLedger() {
        this.transactions = [];
        console.log("Ledger cleared.");
    }

    enhanceProtection(amount) {
        this.ces.enhanceProtection(amount);
    }

    getProtectionLevel() {
        return this.ces.getProtectionLevel();
    }

    resetProtection() {
        this.ces.resetProtection();
    }

    triggerSelfHealing() {
        this.sebd.selfHeal();
        console.log("Self-healing process triggered in the blockchain.");
    }

    reverseLedgerEntropy() {
        this.transactions = this.transactions.map(transaction => {
            const reversedData = this.gers.reverseEntropy(transaction.data);
            return { ...transaction, data: reversedData };
        });
        console.log("Entropy reversed on all ledger transactions.");
    }

    queryIHDV(currentTime) {
        return this.ihdv.queryData(currentTime);
    }

    // Method to get the status of the ERCF
    getContinuityFieldStatus() {
        return this.erfc.getStatus();
    }

    // Method to protect against cosmic entropy using ERCF
    protectAgainstEntropy(currentEntropyLevel) {
        this.erfc.protectAgainstEntropy(currentEntropyLevel);
    }
}

export default HolographicQuantumLedger;
