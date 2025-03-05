const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('PiConverter Contract', function () {
    let PiConverter;
    let piConverter;
    let owner;
    let addr1;
    let addr2;

    beforeEach(async function () {
        // Get the ContractFactory and Signers here.
        PiConverter = await ethers.getContractFactory('PiConverter');
        [owner, addr1, addr2] = await ethers.getSigners();

        // Deploy a new PiConverter contract before each test
        piConverter = await PiConverter.deploy(100, 2, owner.address); // Initial rate, fee percentage, fee collector
        await piConverter.deployed();
    });

    describe('Deployment', function () {
        it('Should set the right owner', async function () {
            expect(await piConverter.owner()).to.equal(owner.address);
        });

        it('Should set the initial conversion rate', async function () {
            expect(await piConverter.conversionRate()).to.equal(100);
        });

        it('Should set the initial fee percentage', async function () {
            expect(await piConverter.feePercentage()).to.equal(2);
        });

        it('Should set the initial fee collector', async function () {
            expect(await piConverter.feeCollector()).to.equal(owner.address);
        });
    });

    describe('Deposits', function () {
        it('Should allow users to deposit Pi Coin', async function () {
            await piConverter.connect(addr1).deposit(100);
            expect(await piConverter.balances(addr1.address)).to.equal(100);
        });

        it('Should emit a Deposited event', async function () {
            await expect(piConverter.connect(addr1).deposit(100))
                .to.emit(piConverter, 'Deposited')
                .withArgs(addr1.address, 100);
        });
    });

    describe('Conversions', function () {
        beforeEach(async function () {
            await piConverter.connect(addr1).deposit(100); // Deposit before testing conversion
        });

        it('Should allow users to convert Pi Coin', async function () {
            await piConverter.connect(addr1).convert(100);
            expect(await piConverter.balances(addr1.address)).to.equal(0); // Balance should be 0 after conversion
        });

        it('Should emit a Converted event', async function () {
            await expect(piConverter.connect(addr1).convert(100))
                .to.emit(piConverter, 'Converted')
                .withArgs(addr1.address, 100, 98, 2); // amount, convertedAmount, fee
        });

        it('Should revert if user has insufficient balance', async function () {
            await expect(piConverter.connect(addr2).convert(100)).to.be.revertedWith('Insufficient balance');
        });
    });

    describe('Fee Management', function () {
        it('Should allow the owner to update the conversion rate', async function () {
            await piConverter.connect(owner).updateConversionRate(200);
            expect(await piConverter.conversionRate()).to.equal(200);
        });

        it('Should allow the owner to update the fee percentage', async function () {
            await piConverter.connect(owner).updateFeePercentage(5);
            expect(await piConverter.feePercentage()).to.equal(5);
        });

        it('Should revert if non-owner tries to update the conversion rate', async function () {
            await expect(piConverter.connect(addr1).updateConversionRate(200)).to.be.revertedWith('Only the owner can perform this action');
        });

        it('Should revert if non-owner tries to update the fee percentage', async function () {
            await expect(piConverter.connect(addr1).updateFeePercentage(5)).to.be.revertedWith('Only the owner can perform this action');
        });
    });

    describe('Fee Collector Management', function () {
        it('Should allow the owner to update the fee collector', async function () {
            await piConverter.connect(owner).updateFeeCollector(addr1.address);
            expect(await piConverter.feeCollector()).to.equal(addr1.address);
        });

        it('Should revert if non-owner tries to update the fee collector', async function () {
            await expect(piConverter.connect(addr1).updateFeeCollector(addr2.address)).to.be.revertedWith('Only the owner can perform this action');
        });
    });
});
