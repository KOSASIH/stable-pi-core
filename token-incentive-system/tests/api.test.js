// tests/api.test.js

const request = require('supertest');
const app = require('../config/server'); // Adjust the path as necessary

describe('API Endpoints', function () {
    it('GET / should return API status', async function () {
        const res = await request(app).get('/');
        expect(res.status).to.equal(200);
        expect(res.text).to.equal('API is running...');
    });

    it('POST /stake should allow users to stake tokens', async function () {
        const res = await request(app)
            .post('/stake')
            .send({ user: '0xAddress', amount: '50' }); // Replace with actual address
        expect(res.status).to.equal(200);
        expect(res.body.message).to.equal('Tokens staked successfully');
    });

    it('POST /unstake should allow users to unstake tokens', async function () {
        const res = await request(app)
            .post('/unstake')
            .send({ user: '0xAddress' }); // Replace with actual address
        expect(res.status).to.equal(200);
        expect(res.body.message).to.equal('Tokens unstaked successfully');
    });
});
