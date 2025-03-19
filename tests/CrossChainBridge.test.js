// tests/CrossChainBridge.test.js

const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('CrossChainBridge', function () {
    let CrossChainBridge;
    let bridge;
    let owner;
    let addr1;
    let addr2;

    const initialDeposit = ethers.utils.parseEther('1.0');
    const withdrawalAmount = ethers.utils.parseEther('0.5');
    const feePercentage = 2; // 2% fee

    beforeEach(async function () {
        CrossChainBridge = await ethers.getContractFactory('CrossChainBridge');
        [owner, addr1, addr2] = await ethers.getSigners();
        bridge = await CrossChainBridge.deploy(feePercentage);
        await bridge.deployed();
    });

    describe('Deployment', function () {
        it('Should set the right owner', async function () {
            expect(await bridge.owner()).to.equal(owner.address);
        });

        it('Should set the correct fee percentage', async function () {
            expect(await bridge.feePercentage()).to.equal(feePercentage);
        });
    });

    describe('Transactions', function () {
        it('Should deposit tokens and emit Deposit event', async function () {
            await expect(bridge.connect(addr1).deposit({ value: initialDeposit }))
                .to.emit(bridge, 'Deposit')
                .withArgs(addr1.address, initialDeposit);

            expect(await bridge.getBalance(addr1.address)).to.equal(initialDeposit);
        });

        it('Should withdraw tokens and emit Withdraw event', async function () {
            await bridge.connect(addr1).deposit({ value: initialDeposit });
            await expect(bridge.connect(addr1).withdraw(withdrawalAmount))
                .to.emit(bridge, 'Withdraw')
                .withArgs(addr1.address, withdrawalAmount);

            expect(await bridge.getBalance(addr1.address)).to.equal(initialDeposit.sub(withdrawalAmount));
        });

        it('Should fail if withdrawal exceeds balance', async function () {
            await bridge.connect(addr1).deposit({ value: initialDeposit });
            await expect(bridge.connect(addr1).withdraw(initialDeposit.add(1))).to.be.revertedWith('Insufficient balance');
        });

        it('Should calculate the correct fee on withdrawal', async function () {
            await bridge.connect(addr1).deposit({ value: initialDeposit });
            const fee = await bridge.calculateFee(withdrawalAmount);
            const expectedBalanceAfterFee = initialDeposit.sub(withdrawalAmount).sub(fee);

            await bridge.connect(addr1).withdraw(withdrawalAmount);
            expect(await bridge.getBalance(addr1.address)).to.equal(expectedBalanceAfterFee);
        });

        it('Should revert if non-owner tries to change fee', async function () {
            await expect(bridge.connect(addr1).setFeePercentage(5)).to.be.revertedWith('Ownable: caller is not the owner');
        });
    });

    describe('Performance Tests', function () {
        it('Should handle multiple deposits efficiently', async function () {
            const depositCount = 100;
            const depositPromises = [];

            for (let i = 0; i < depositCount; i++) {
                depositPromises.push(bridge.connect(addr1).deposit({ value: ethers.utils.parseEther('0.01') }));
            }

            const start = performance.now();
            await Promise.all(depositPromises);
            const end = performance.now();

            console.log(`Time taken for ${depositCount} deposits: ${end - start} ms`);
        });
    });

    describe('Edge Cases', function () {
        it('Should handle zero withdrawal gracefully', async function () {
            await bridge.connect(addr1).deposit({ value: initialDeposit });
            await bridge.connect(addr1).withdraw(0);
            expect(await bridge.getBalance(addr1.address)).to.equal(initialDeposit);
        });

        it('Should revert on invalid address', async function () {
            await expect(bridge.connect(addr1).deposit({ value: initialDeposit, to: '0x0' })).to.be.revertedWith('Invalid address');
        });
    });
});
