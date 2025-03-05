const request = require('supertest');
const { expect } = require('chai');
const app = require('../../src/app'); // Import your Express app
const mongoose = require('mongoose');
const User = require('../../src/models/User');
const Transaction = require('../../src/models/Transaction');

describe('API Integration Tests', () => {
    before(async () => {
        // Connect to the database before running tests
        await mongoose.connect(process.env.DB_URI || 'mongodb://localhost:27017/piCoinDB', {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
    });

    after(async () => {
        // Clean up the database and close the connection after tests
        await User.deleteMany({});
        await Transaction.deleteMany({});
        await mongoose.connection.close();
    });

    describe('POST /api/users', () => {
        it('should create a new user', async () => {
            const res = await request(app)
                .post('/api/users')
                .send({ walletAddress: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef' });

            expect(res.status).to.equal(201);
            expect(res.body).to.have.property('walletAddress', '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef');
        });

        it('should return an error for duplicate wallet address', async () => {
            await request(app)
                .post('/api/users')
                .send({ walletAddress: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef' });

            const res = await request(app)
                .post('/api/users')
                .send({ walletAddress: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef' });

            expect(res.status).to.equal(400);
            expect(res.body).to.have.property('error', 'User  already exists');
        });
    });

    describe('POST /api/transactions', () => {
        let userId;

        before(async () => {
            // Create a user to associate with the transaction
            const user = new User({ walletAddress: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef' });
            await user.save();
            userId = user._id;
        });

        it('should create a new transaction', async () => {
            const res = await request(app)
                .post('/api/transactions')
                .send({
                    userId,
                    type: 'deposit',
                    amount: 100,
                    transactionHash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
                });

            expect(res.status).to.equal(201);
            expect(res.body).to.have.property('amount', 100);
            expect(res.body).to.have.property('type', 'deposit');
        });

        it('should return an error for invalid userId', async () => {
            const res = await request(app)
                .post('/api/transactions')
                .send({
                    userId: 'invalidUser Id',
                    type: 'deposit',
                    amount: 100,
                    transactionHash: '0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef',
                });

            expect(res.status).to.equal(400);
            expect(res.body).to.have.property('error', 'Invalid user ID');
        });
    });

    describe('GET /api/users/:id', () => {
        let userId;

        before(async () => {
            // Create a user to test the retrieval
            const user = new User({ walletAddress: '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef' });
            await user.save();
            userId = user._id;
        });

        it('should retrieve a user by ID', async () => {
            const res = await request(app).get(`/api/users/${userId}`);

            expect(res.status).to.equal(200);
            expect(res.body).to.have.property('walletAddress', '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef');
        });

        it('should return an error for invalid user ID', async () => {
            const res = await request(app).get('/api/users/invalidUser Id');

            expect(res.status).to.equal(404);
            expect(res.body).to.have.property('error', 'User  not found');
        });
    });
});
