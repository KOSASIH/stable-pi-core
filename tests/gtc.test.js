// tests/gtc.test.js
const gtc = require('../src/tokens/gtc');
const GalacticWallet = require('../src/tokens/wallet');

test('GTC and GU transfers work', async () => {
  await gtc.initialize();
  const wallet1 = new GalacticWallet("0xTest1");
  const wallet2 = new GalacticWallet("0xTest2");

  await gtc.transferGTC(gtc.owner, wallet1.address, 100); // 100 GTC
  await wallet1.sendGU(wallet2.address, 31415.9); // 31415.9 GU = $31,415.9

  const balance1 = wallet1.checkBalance();
  const balance2 = wallet2.checkBalance();

  expect(balance1.GTC).toBeCloseTo(99.9, 1); // 100 - 0.1 GTC
  expect(balance2.GU).toBe(31415.9); // 31415.9 GU
});
