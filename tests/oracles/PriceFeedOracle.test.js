// tests/oracles/PriceFeedOracle.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("PriceFeedOracle", function () {
    let PriceFeedOracle;
    let priceFeedOracle;
    let owner;
    let addr1;

    beforeEach(async function () {
        [owner, addr1] = await ethers.getSigners();

        // Deploy the PriceFeedOracle contract
        PriceFeedOracle = await ethers.getContractFactory("PriceFeedOracle");
        priceFeedOracle = await PriceFeedOracle.deploy(18, "Price Feed for PiCoin");
        await priceFeedOracle.deployed();
    });

    it("should set the correct decimals and description", async function () {
        expect(await priceFeedOracle.decimals()).to.equal(18);
        expect(await priceFeedOracle.description()).to.equal("Price Feed for PiCoin");
    });

    it("should allow the owner to update the price", async function () {
        await priceFeedOracle.setPrice(ethers.utils.parseUnits("300000", 18)); // Set price
        const price = await priceFeedOracle.getLatestPrice();
        expect(price).to.equal(ethers.utils.parseUnits("300000", 18));
    });

    it("should not allow non-owners to update the price", async function () {
        await expect(priceFeedOracle.connect(addr1).setPrice(ethers.utils.parseUnits("300000", 18))).to.be.revertedWith("Ownable: caller is not the owner");
    });

    it("should return the latest price correctly", async function () {
        await priceFeedOracle.setPrice(ethers.utils.parseUnits("300000", 18)); // Set price
        const price = await priceFeedOracle.getLatestPrice();
        expect(price).to.equal(ethers.utils.parseUnits("300000", 18));
    });
});
