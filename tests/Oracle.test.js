const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Oracle Contract", function () {
    let Oracle;
    let oracleInstance;
    let owner;
    let oracle1;
    let oracle2;

    beforeEach(async function () {
        // Get the ContractFactory and Signers here.
        Oracle = await ethers.getContractFactory("Oracle");
        [owner, oracle1, oracle2] = await ethers.getSigners();

        // Deploy a new Oracle contract for each test
        oracleInstance = await Oracle.deploy();
        await oracleInstance.deployed();
    });

    describe("Deployment", function () {
        it("Should deploy the contract and set the owner as admin and oracle", async function () {
            expect(await oracleInstance.hasRole(await oracleInstance.ADMIN_ROLE(), owner.address)).to.be.true;
            expect(await oracleInstance.hasRole(await oracleInstance.ORACLE_ROLE(), owner.address)).to.be.true;
        });
    });

    describe("Role Management", function () {
        it("Should allow the owner to add oracles", async function () {
            await oracleInstance.grantRole(await oracleInstance.ORACLE_ROLE(), oracle1.address);
            expect(await oracleInstance.hasRole(await oracleInstance.ORACLE_ROLE(), oracle1.address)).to.be.true;
        });

        it("Should not allow non-admin to add oracles", async function () {
            await expect(oracleInstance.connect(oracle1).grantRole(await oracleInstance.ORACLE_ROLE(), oracle2.address))
                .to.be.revertedWith("AccessControl: sender must be an admin to grant");
        });
    });

    describe("Data Submission", function () {
        beforeEach(async function () {
            // Grant oracle1 the oracle role
            await oracleInstance.grantRole(await oracleInstance.ORACLE_ROLE(), oracle1.address);
        });

        it("Should allow oracles to submit data", async function () {
            await oracleInstance.connect(oracle1).submitData("ETH/USD", "3000");
            const data = await oracleInstance.getData("ETH/USD");
            expect(data[0]).to.equal("3000");
            expect(data[1]).to.be.greaterThan(0); // Check timestamp
            expect(data[2]).to.include(oracle1.address); // Check oracle address
        });

        it("Should require data type and data to be non-empty", async function () {
            await expect(oracleInstance.connect(oracle1).submitData("", "3000"))
                .to.be.revertedWith("Data type cannot be empty");
            await expect(oracleInstance.connect(oracle1).submitData("ETH/USD", ""))
                .to.be.revertedWith("Data cannot be empty");
        });

        it("Should require multiple confirmations for data to be valid", async function () {
            await oracleInstance.connect(oracle1).submitData("ETH/USD", "3000");
            await oracleInstance.grantRole(await oracleInstance.ORACLE_ROLE(), oracle2.address);
            await oracleInstance.connect(oracle2).submitData("ETH/USD", "3000");

            const data = await oracleInstance.getData("ETH/USD");
            expect(data[0]).to.equal("3000");
            expect(data[2]).to.include(oracle1.address);
            expect(data[2]).to.include(oracle2.address);
        });

        it("Should not allow the same oracle to submit data multiple times for the same type", async function () {
            await oracleInstance.connect(oracle1).submitData("ETH/USD", "3000");
            await expect(oracleInstance.connect(oracle1).submitData("ETH/USD", "3100"))
                .to.be.revertedWith("Oracle has already submitted data for this type");
        });
    });

    describe("Data Retrieval", function () {
        beforeEach(async function () {
            await oracleInstance.grantRole(await oracleInstance.ORACLE_ROLE(), oracle1.address);
            await oracleInstance.connect(oracle1).submitData("ETH/USD", "3000");
        });

        it("Should retrieve the correct data", async function () {
            const data = await oracleInstance.getData("ETH/USD");
            expect(data[0]).to.equal("3000");
            expect(data[1]).to.be.greaterThan(0); // Check timestamp
            expect(data[2]).to.include(oracle1.address); // Check oracle address
        });

        it("Should revert if no data is found for the given type", async function () {
            await expect(oracleInstance.getData("BTC/USD"))
                .to.be.revertedWith("No data found for this type");
        });
    });

    describe("Data Deletion", function () {
        before ```javascript
        beforeEach(async function () {
            await oracleInstance.grantRole(await oracleInstance.ORACLE_ROLE(), oracle1.address);
            await oracleInstance.connect(oracle1).submitData("ETH/USD", "3000");
        });

        it("Should allow the owner to delete data", async function () {
            await oracleInstance.deleteData("ETH/USD");
            await expect(oracleInstance.getData("ETH/USD"))
                .to.be.revertedWith("No data found for this type");
        });

        it("Should not allow non-admin to delete data", async function () {
            await expect(oracleInstance.connect(oracle1).deleteData("ETH/USD"))
                .to.be.revertedWith("AccessControl: sender must be an admin to revoke");
        });
    });
});
