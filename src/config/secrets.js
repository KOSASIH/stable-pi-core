// config/secrets.js

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

// Load secrets from a secure file
const secretsFilePath = path.resolve(__dirname, '../secrets.json');

let secrets = {};

if (fs.existsSync(secretsFilePath)) {
    const rawData = fs.readFileSync(secretsFilePath);
    secrets = JSON.parse(rawData);
} else {
    throw new Error("Secrets file not found. Please create a secrets.json file.");
}

// Function to encrypt sensitive data
export function encrypt(data) {
    const algorithm = 'aes-256-cbc';
    const key = crypto.scryptSync(process.env.SECRET_KEY, 'salt', 32);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(algorithm, key, iv);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return { iv: iv.toString('hex'), encryptedData: encrypted };
}

// Function to decrypt sensitive data
export function decrypt(encryptedData) {
    const algorithm = 'aes-256-cbc';
    const key = crypto.scryptSync(process.env.SECRET_KEY, 'salt', 32);
    const decipher = crypto.createDecipheriv(algorithm, key, Buffer.from(encryptedData.iv, 'hex'));
    let decrypted = decipher.update(encryptedData.encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

// Export secrets securely
export const getSecret = (key) => {
    if (!secrets[key]) {
        throw new Error(`Secret for ${key} not found.`);
    }
    return decrypt(secrets[key]);
};
