// src/tests/qvt.test.js
const QuantumVortexTransatron = require('./qvt');
const { starEnergy } = require('../tokens/starEnergy');
const { cnc } = require('../tokens/cnc');
const { tcp } = require('../quantum/tcp');

jest.mock('../tokens/starEnergy');
jest.mock('../tokens/cnc');
jest.mock('../quantum/tcp');

describe('Quantum Vortex Transatron', () => {
  let qvt;

  beforeEach(() => {
    qvt = QuantumVortexTransatron;
    qvt.activate();
  });

  afterEach(() => {
    qvt.deactivate();
  });

  test('should activate the QVT', () => {
    expect(qvt.active).toBe(true);
  });

  test('should initialize vortex locations', () => {
    expect(qvt.vortexLocations.size).toBeGreaterThan(0);
    expect(qvt.vortexLocations.has('Earth Orbit')).toBe(true);
    expect(qvt.vortexLocations.has('Mars Surface')).toBe(true);
  });

  test('should add a new vortex location', () => {
    qvt.addVortex('Jupiter Orbit');
    expect(qvt.vortexLocations.has('Jupiter Orbit')).toBe(true);
  });

  test('should not add an existing vortex location', () => {
    qvt.addVortex('Earth Orbit');
    expect(qvt.vortexLocations.size).toBe(3); // Should remain the same
  });

  test('should remove a vortex location', () => {
    qvt.removeVortex('Earth Orbit');
    expect(qvt.vortexLocations.has('Earth Orbit')).toBe(false);
  });

  test('should not remove a non-existing vortex location', () => {
    qvt.removeVortex('Non-Existing Location');
    expect(qvt.vortexLocations.size).toBe(3); // Should remain the same
  });

  test('should transport Star Energy successfully', async () => {
    starEnergy.transfer.mockResolvedValue(true);
    tcp.send.mockResolvedValue(true);

    await qvt.transportAsset('Earth Orbit', 'Mars Surface', 'StarEnergy', 5, { isAuthenticated: true });

    expect(starEnergy.transfer).toHaveBeenCalledWith(starEnergy.owner, 'system-reserve', 5);
    expect(tcp.send).toHaveBeenCalledWith({
      event: 'TRANSPORT',
      asset: 'StarEnergy',
      amount: 5,
      from: 'Earth Orbit',
      to: 'Mars Surface',
    });
    expect(qvt.transactionHistory.length).toBe(1);
  });

  test('should transport CNC successfully', async () => {
    cnc.transfer.mockResolvedValue(true);
    tcp.send.mockResolvedValue(true);

    await qvt.transportAsset('Mars Surface', 'Proxima Centauri', 'CNC', 10, { isAuthenticated: true });

    expect(cnc.transfer).toHaveBeenCalledWith(cnc.owner, 'system-reserve', 10);
    expect(tcp.send).toHaveBeenCalledWith({
      event: 'TRANSPORT',
      asset: 'CNC',
      amount: 10,
      from: 'Mars Surface',
      to: 'Proxima Centauri',
    });
    expect(qvt.transactionHistory.length).toBe(1);
  });

  test('should throw an error for unauthorized user', async () => {
    await expect(qvt.transportAsset('Earth Orbit', 'Mars Surface', 'StarEnergy', 5, { isAuthenticated: false }))
      .rejects
      .toThrow('Unauthorized user');
  });

  test('should throw an error for non-existing vortex location', async () => {
    await expect(qvt.transportAsset('Non-Existing Location', 'Mars Surface', 'StarEnergy', 5, { isAuthenticated: true }))
      .rejects
      .toThrow('Vortex location not found');
  });

  test('should log transactions correctly', async () => {
    starEnergy.transfer.mockResolvedValue(true);
    tcp.send.mockResolvedValue(true);

    await qvt.transportAsset('Earth Orbit', 'Mars Surface', 'Star Energy', 5, { isAuthenticated: true });

    const lastTransaction = qvt.transactionHistory[qvt.transactionHistory.length - 1];
    expect(lastTransaction.assetType).toBe('StarEnergy');
    expect(lastTransaction.amount).toBe(5);
    expect(lastTransaction.fromLocation).toBe('Earth Orbit');
    expect(lastTransaction.toLocation).toBe('Mars Surface');
    expect(new Date(lastTransaction.timestamp)).toBeInstanceOf(Date);
  });

  test('should handle transport errors gracefully', async () => {
    starEnergy.transfer.mockRejectedValue(new Error('Transfer failed'));

    await expect(qvt.transportAsset('Earth Orbit', 'Mars Surface', 'StarEnergy', 5, { isAuthenticated: true }))
      .rejects
      .toThrow('Transport failed');
  });
});
