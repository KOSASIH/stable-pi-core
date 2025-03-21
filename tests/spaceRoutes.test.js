// tests/spaceRoutes.test.js

import request from 'supertest';
import express from 'express';
import spaceRoutes from '../src/routes/spaceRoutes';
import AntimatterPropulsionNetwork from '../src/space/apn';
import NeutrinoBasedCommunicationArray from '../src/space/neutrinoComm';

const app = express();
app.use(express.json());
app.use('/space', spaceRoutes);

const apn = new AntimatterPropulsionNetwork();
const neutrinoComm = new NeutrinoBasedCommunicationArray();

describe('Space Routes', () => {
    beforeEach(() => {
        // Clear nodes and message queue before each test
        apn.nodes = [];
        neutrinoComm.nodes = [];
        neutrinoComm.messageQueue = [];
    });

    test('POST /space/add-node - should add a new node', async () => {
        const response = await request(app)
            .post('/space/add-node')
            .send({ name: 'Node1' });

        expect(response.status).toBe(201);
        expect(response.body.success).toBe(true);
        expect(response.body.message).toBe('Node Node1 added successfully.');
    });

    test('POST /space/add-node - should not add duplicate node', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });

        const response = await request(app)
            .post('/space/add-node')
            .send({ name: 'Node1' });

        expect(response.status).toBe(400);
        expect(response.body.success).toBe(false);
        expect(response.body.message).toBe('Node Node1 already exists in the communication array.');
    });

    test('POST /space/initiate-propulsion - should initiate propulsion for a node', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });

        const response = await request(app)
            .post('/space/initiate-propulsion')
            .send({ nodeName: 'Node1', targetOrbit: 'Jupiter' });

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(response.body.message).toBe('Node1 has reached orbit Jupiter.');
    });

    test('POST /space/initiate-propulsion - should return error for non-existent node', async () => {
        const response = await request(app)
            .post('/space/initiate-propulsion')
            .send({ nodeName: 'Node2', targetOrbit: 'Jupiter' });

        expect(response.status).toBe(400);
        expect(response.body.success).toBe(false);
        expect(response.body.message).toBe('Node Node2 not found in the network.');
    });

    test('POST /space/send-message - should send a message to a node', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });

        const response = await request(app)
            .post('/space/send-message')
            .send({ nodeName: 'Node1', message: 'Hello, Node1!' });

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(response.body.message).toBe('Message sent to Node1.');
    });

    test('POST /space/send-message - should return error for non-existent node', async () => {
        const response = await request(app)
            .post('/space/send-message')
            .send({ nodeName: 'Node2', message: 'Hello, Node2!' });

        expect(response.status).toBe(400);
        expect(response.body.success).toBe(false);
        expect(response.body.message).toBe('Node Node2 not found in the communication array.');
    });

    test('GET /space/node-status/:nodeName - should return status of a specific node', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });

        const response = await request(app).get('/space/node-status/Node1');

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(response.body.status).toHaveProperty('name', 'Node1');
    });

    test('GET /space/node-status/:nodeName - should return error for non-existent node', async () => {
        const response = await request(app).get('/space/node-status/Node2');

        expect(response.status).toBe(404);
        expect(response.body.success).toBe(false);
        expect(response.body.message).toBe('Node Node2 not found in the network.');
    });

    test('GET /space/all-nodes-status - should return status of all nodes', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });
        await request(app).post('/space/add-node').send({ name: 'Node2' });

        const response = await request(app).get('/space/all-nodes-status');

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(response.body.allStatus.length).toBe(2);
    });

    test('GET /space/message-queue - should return the message queue', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });
        await request(app).post('/space/send-message').send({ nodeName: 'Node1', message: 'Test message' });

        const response = await request(app).get('/space/message-queue');

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(response.body.queue.length).toBe(1);
    });

    test('DELETE /space/clear-message-queue - should clear the message queue', async () => {
        await request(app).post('/space/add-node').send({ name: 'Node1' });
        await request(app).post('/space/send-message').send({ nodeName: 'Node1', message: 'Test message' });

        await request(app).delete('/space/clear-message-queue');

        const response = await request(app).get('/space/message-queue');

        expect(response.status).toBe(200);
        expect(response.body.success).toBe(true);
        expect(response.body.queue.length).toBe(0);
    });
});
