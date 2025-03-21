// src/routes/spaceRoutes.js

import express from 'express';
import AntimatterPropulsionNetwork from '../space/apn';
import NeutrinoBasedCommunicationArray from '../space/neutrinoComm';

const router = express.Router();
const apn = new AntimatterPropulsionNetwork();
const neutrinoComm = new NeutrinoBasedCommunicationArray();

// Endpoint to add a new node
router.post('/add-node', (req, res) => {
    const { name } = req.body;
    try {
        apn.addNode({ name });
        neutrinoComm.addNode({ name });
        res.status(201).json({ success: true, message: `Node ${name} added successfully.` });
    } catch (error) {
        res.status(400).json({ success: false, message: error.message });
    }
});

// Endpoint to initiate propulsion for a node
router.post('/initiate-propulsion', async (req, res) => {
    const { nodeName, targetOrbit } = req.body;
    try {
        await apn.initiatePropulsion(nodeName, targetOrbit);
        res.json({ success: true, message: `${nodeName} has reached orbit ${targetOrbit}.` });
    } catch (error) {
        res.status(400).json({ success: false, message: error.message });
    }
});

// Endpoint to send a message to a node
router.post('/send-message', async (req, res) => {
    const { nodeName, message } = req.body;
    try {
        await neutrinoComm.sendMessage(nodeName, message);
        res.json({ success: true, message: `Message sent to ${nodeName}.` });
    } catch (error) {
        res.status(400).json({ success: false, message: error.message });
    }
});

// Endpoint to get the status of a specific node
router.get('/node-status/:nodeName', (req, res) => {
    const { nodeName } = req.params;
    try {
        const status = apn.getNodeStatus(nodeName);
        res.json({ success: true, status });
    } catch (error) {
        res.status(404).json({ success: false, message: error.message });
    }
});

// Endpoint to get the status of all nodes
router.get('/all-nodes-status', (req, res) => {
    try {
        const allStatus = apn.getAllNodesStatus();
        res.json({ success: true, allStatus });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Endpoint to retrieve the message queue
router.get('/message-queue', (req, res) => {
    try {
        const queue = neutrinoComm.getMessageQueue();
        res.json({ success: true, queue });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

// Endpoint to clear the message queue
router.delete('/clear-message-queue', (req, res) => {
    try {
        neutrinoComm.clearMessageQueue();
        res.json({ success: true, message: "Message queue cleared." });
    } catch (error) {
        res.status(500).json({ success: false, message: error.message });
    }
});

export default router;
