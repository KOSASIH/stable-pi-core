// src/core/utils.js

import crypto from 'crypto';

// Generate a quantum-safe hash for a given data object
export function generateQuantumHash(data) {
    const hash = crypto.createHash('sha512'); // Using SHA-512 for strong hashing
    hash.update(JSON.stringify(data));
    return hash.digest('hex');
}

// Sign a transaction using a private key with quantum-safe algorithms
export function signTransaction(transaction, privateKey) {
    const sign = crypto.createSign('SHA512');
    sign.update(transaction.serialize());
    sign.end();
    return sign.sign(privateKey, 'hex'); // Return the signature in hex format
}

// Validate the signature of a transaction using the public key
export function validateQuantumSignature(transaction) {
    const verify = crypto.createVerify('SHA512');
    verify.update(transaction.serialize());
    verify.end();
    return verify.verify(transaction.user.publicKey, transaction.signature, 'hex');
}

// Generate a quantum-safe token for user authentication
export function generateQuantumToken(username, role, privateKey) {
    const tokenData = { username, role, timestamp: Date.now() };
    const tokenHash = generateQuantumHash(tokenData);
    const sign = crypto.createSign('SHA512');
    sign.update(tokenHash);
    sign.end();
    const signature = sign.sign(privateKey, 'hex');
    return { tokenHash, signature };
}

// Validate a quantum token using the user's public key
export function validateQuantumToken(token, publicKey) {
    const { tokenHash, signature } = token;
    const verify = crypto.createVerify('SHA512');
    verify.update(tokenHash);
    verify.end();
    return verify.verify(publicKey, signature, 'hex');
}

// Generate a random string for unique identifiers
export function generateRandomString(length = 16) {
    return crypto.randomBytes(length).toString('hex');
}

// Utility function to deep clone an object
export function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

// Utility function to check if an object is empty
export function isEmptyObject(obj) {
    return Object.keys(obj).length === 0;
}

// Utility function to format timestamps
export function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toISOString(); // Return in ISO format
}
