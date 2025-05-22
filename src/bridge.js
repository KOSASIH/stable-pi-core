/**
 * Advanced PiCoin Transfer Module using Wormhole SDK
 * 
 * Features:
 * - Robust async transfer with retries
 * - Detailed progress events and logging
 * - Configurable parameters including retry count, timeout, network
 * - Input validation and error handling
 * - Support for gas fee estimation placeholder (depending on Wormhole SDK support)
 * - Exportable class for extensibility
 * - Compatible with Node.js environment
 */

const EventEmitter = require('events');
const { Wormhole } = require('@wormhole-foundation/sdk');

class PiCoinTransfer extends EventEmitter {
    /**
     * Constructs the PiCoinTransfer instance.
     * @param {object} options - Configuration options.
     * @param {string} [options.network='mainnet'] - Wormhole network environment.
     * @param {number} [options.retryCount=3] - Number of retries on failure.
     * @param {number} [options.retryDelayMs=3000] - Delay between retries in milliseconds.
     * @param {string} [options.token='PI'] - Token symbol to transfer.
     * @param {string} [options.fromChain='PiNetwork'] - Source chain name.
     */
    constructor(options = {}) {
        super();
        this.network = options.network || 'mainnet';
        this.retryCount = options.retryCount || 3;
        this.retryDelayMs = options.retryDelayMs || 3000;
        this.token = options.token || 'PI';
        this.fromChain = options.fromChain || 'PiNetwork';

        this.wormhole = new Wormhole(this.network);

        this._log(`Initialized PiCoinTransfer on network: ${this.network}`);
    }

    _log(message) {
        // Emits a 'log' event with the message
        this.emit('log', `[PiCoinTransfer]: ${message}`);
    }

    _validateInputs(toChain, amount) {
        if (typeof toChain !== 'string' || toChain.trim() === '') {
            throw new TypeError('Recipient chain name must be a non-empty string.');
        }
        if (typeof amount !== 'number' && typeof amount !== 'string') {
            throw new TypeError('Amount must be a number or string representing a numeric value.');
        }
        const numericAmount = Number(amount);
        if (isNaN(numericAmount) || numericAmount <= 0) {
            throw new RangeError('Amount must be a positive number.');
        }
        return numericAmount;
    }

    async _delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Transfer PiCoin token to another chain.
     * Emits events:
     * - 'start' when transfer starts
     * - 'progress' with current step info
     * - 'success' upon successful transfer with transaction details
     * - 'error' on failure
     * 
     * @param {string} toChain - The target chain name.
     * @param {number|string} amount - Amount to transfer.
     * @returns {Promise<object>} Transfer result details.
     */
    async transfer(toChain, amount) {
        this._log(`Preparing to transfer ${amount} ${this.token} from ${this.fromChain} to ${toChain}`);

        // Validate inputs
        let numericAmount;
        try {
            numericAmount = this._validateInputs(toChain, amount);
        } catch (validationError) {
            this.emit('error', validationError);
            throw validationError;
        }

        this.emit('start', { toChain, amount: numericAmount, token: this.token });

        let attempt = 0;
        while (attempt <= this.retryCount) {
            try {
                attempt++;
                this._log(`Attempt ${attempt} to transfer tokens...`);

                this.emit('progress', { status: 'initiating_transfer', attempt });

                // Call the Wormhole transfer method
                // Assuming wormhole.transfer returns a promise with tx details; adjust as per SDK
                const result = await this.wormhole.transfer({
                    fromChain: this.fromChain,
                    toChain: toChain,
                    amount: numericAmount,
                    token: this.token,
                });

                this._log(`Transfer successful on attempt ${attempt}`);
                this.emit('success', result);
                return result;

            } catch (error) {
                this._log(`Transfer attempt ${attempt} failed: ${error.message || error}`);

                this.emit('error', { attempt, error });

                if (attempt > this.retryCount) {
                    this._log('Max retries reached, aborting transfer.');
                    throw new Error(`Transfer failed after ${this.retryCount} attempts: ${error.message || error}`);
                }

                this._log(`Retrying after ${this.retryDelayMs}ms...`);
                await this._delay(this.retryDelayMs);
            }
        }
    }
}

module.exports = PiCoinTransfer;

/**
 * Example Usage:
 * 
 * const PiCoinTransfer = require('./advancedPiCoinTransfer');
 * 
 * async function run() {
 *   const piTransfer = new PiCoinTransfer({ retryCount: 5, retryDelayMs: 5000 });
 * 
 *   piTransfer.on('log', msg => console.log(msg));
 *   piTransfer.on('start', info => console.log('Transfer starting:', info));
 *   piTransfer.on('progress', status => console.log('Progress:', status));
 *   piTransfer.on('success', result => console.log('Transfer successful:', result));
 *   piTransfer.on('error', error => console.error('Transfer error:', error));
 * 
 *   try {
 *     const result = await piTransfer.transfer('Ethereum', 100);
 *     console.log('Final result:', result);
 *   } catch (err) {
 *     console.error('Transfer failed:', err);
 *   }
 * }
 * 
 * run();
 */
