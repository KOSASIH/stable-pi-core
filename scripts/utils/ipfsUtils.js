// scripts/utils/ipfsUtils.js

const { create } = require('ipfs-http-client');

// Initialize IPFS client
const ipfs = create({ url: 'https://ipfs.infura.io:5001' });

/**
 * Store data on IPFS
 * @param {Object} data - The data to be stored on IPFS
 * @returns {Promise<string>} - The CID of the stored data
 */
async function storeData(data) {
    try {
        const { cid } = await ipfs.add(JSON.stringify(data));
        console.log(`Data stored on IPFS with CID: ${cid}`);
        return cid.toString();
    } catch (error) {
        console.error('Error storing data on IPFS:', error);
        throw error;
    }
}

/**
 * Retrieve data from IPFS
 * @param {string} cid - The CID of the data to retrieve
 * @returns {Promise<Object>} - The retrieved data
 */
async function retrieveData(cid) {
    try {
        const stream = ipfs.cat(cid);
        let data = '';

        for await (const chunk of stream) {
            data += chunk.toString();
        }

        console.log(`Data retrieved from IPFS with CID: ${cid}`);
        return JSON.parse(data);
    } catch (error) {
        console.error('Error retrieving data from IPFS:', error);
        throw error;
    }
}

/**
 * Delete data from IPFS (Note: IPFS is a decentralized storage system, so data cannot be deleted)
 * This function is a placeholder to indicate that data cannot be deleted from IPFS.
 */
function deleteData() {
    console.warn('Data cannot be deleted from IPFS. Once stored, it remains available.');
}

module.exports = {
    storeData,
    retrieveData,
    deleteData,
};
