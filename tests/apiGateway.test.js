// tests/apiGateway.test.js

const request = require("supertest");
const { expect } = require("chai");
const app = require("../self-healing/apiGateway"); // Adjust the path as necessary

describe("API Gateway", function () {
    it("should add liquidity", async function () {
        const response = await request(app)
            .post("/api/ethereum/addLiquidity")
            .send({ amountA: "100", amountB: "100" });
        expect(response.status).to.equal(200);
        expect(response.body.success).to.be.true;
    });

    it("should swap tokens", async function () {
        const response = await request(app)
            .post("/api/ethereum/swap")
            .send({ amountIn: "10", isAToB: true });
        expect(response.status).to.equal(200);
        expect(response.body.success).to.be.true;
    });
});
