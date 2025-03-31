// src/space/main.js - Ultra Advanced Stable-Pi-Core Main File

const express = require('express');
const bodyParser = require('body-parser');
const { createServer } = require('http');
const { Server } = require('socket.io');
const GalacticGovernanceFramework = require('./ggf'); // Import GGF
const TachyonicCommunicationProtocol = require('./tcp'); // Import TCP
const AstroSentientGovernanceMatrix = require('./asgm'); // Import ASGM
const { validateProposal, validateVote } = require('./validators'); // Import validators

const app = express();
const server = createServer(app);
const io = new Server(server);

const port = process.env.PORT || 3000;
const ggf = new GalacticGovernanceFramework();
const tcp = new TachyonicCommunicationProtocol();

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Initialize the GGF with the tachyonic communication protocol
ggf.initializeGGF(tcp);

// Socket.io connection
io.on('connection', (socket) => {
    console.log('New client connected');

    socket.on('createProposal', (data) => {
        try {
            validateProposal(data); // Validate proposal data
            const proposal = ggf.createProposal(data.title, data.description, data.proposer);
            socket.emit('proposalCreated', proposal);
        } catch (error) {
            socket.emit('error', error.message);
        }
    });

    socket.on('voteOnProposal', (data) => {
        try {
            validateVote(data); // Validate vote data
            ggf.voteOnProposal(data.proposalId, data.entityId);
            socket.emit('voteCast', { proposalId: data.proposalId, entityId: data.entityId });
        } catch (error) {
            socket.emit('error', error.message);
        }
    });

    socket.on('getVotingResults', (proposalId) => {
        try {
            const results = ggf.getVotingResults(proposalId);
            socket.emit('votingResults', results);
        } catch (error) {
            socket.emit('error', error.message);
        }
    });

    socket.on('executeProposal', (proposalId) => {
        try {
            ggf.executeProposal(proposalId);
            socket.emit('proposalExecuted', proposalId);
        } catch (error) {
            socket.emit('error', error.message);
        }
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

// API Endpoints
app.post('/proposals', (req, res) => {
    const { title, description, proposer } = req.body;
    try {
        validateProposal(req.body); // Validate proposal data
        const proposal = ggf.createProposal(title, description, proposer);
        res.status(201).json(proposal);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

app.get('/proposals/:id', (req, res) => {
    const proposalId = req.params.id;
    const proposal = ggf.getProposalById(proposalId);
    if (proposal) {
        res.json(proposal);
    } else {
        res.status(404).json({ error: 'Proposal not found' });
    }
});

// Start the server
server.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

// Example of sending proposals to nodes
const nodes = ['Node1', 'Node2', 'Node3'];
const proposals = ggf.getAllProposals();
ggf.sendProposalsToNodes(proposals, nodes);

// Predict future outcomes using TBPG
const currentData = { growthRate: 3 };
ggf.predictAndSend('economic_growth', currentData, nodes);

// Utilize ASGM for decision making
const asgmDecisions = ggf.utilizeASGM();
console.log('ASGM Decisions:', asgmDecisions);

// Graceful shutdown handling
process.on('SIGINT', () => {
    console.log('Shutting down gracefully...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    // Handle logging and cleanup if necessary
});

module.exports = { app, server, io, ggf };
