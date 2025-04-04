// tests/qvge.test.js
const qvge = require('../src/core/qvge');
const { hql } = require('../src/core/hql'); // Mocking HQL for testing
const { jest } = require('@jest/globals');

jest.mock('../src/core/hql'); // Mocking the HQL module

describe('Quantum Void Genesis Engine Tests', () => {
  beforeEach(() => {
    qvge.deactivate(); // Ensure the engine is deactivated before each test
  });

  test('should activate the Quantum Void Genesis Engine', () => {
    qvge.activate();
    expect(qvge.active).toBe(true);
  });

  test('should generate a void space successfully', async () => {
    qvge.activate();
    const voidId = await qvge.generateVoidSpace('Mars Orbit', 1e21);
    expect(voidId).toMatch(/void-Mars Orbit-\d+/);
    expect(qvge.voidSpaces.size).toBe(1);
    expect(qvge.voidSpaces.get(voidId)).toMatchObject({
      location: 'Mars Orbit',
      capacity: 1e21,
      used: 0,
    });
    expect(hql.storeData).toHaveBeenCalledWith(voidId, expect.any(Object));
  });

  test('should store data in a void space successfully', async () => {
    qvge.activate();
    const voidId = await qvge.generateVoidSpace('Mars Orbit', 1e21);
    const data = { size: 1024 }; // Example data

    await qvge.storeInVoid(voidId, data);
    expect(qvge.voidSpaces.get(voidId).used).toBe(1024);
    expect(hql.storeData).toHaveBeenCalledWith(`${voidId}-data`, data);
  });

  test('should throw an error when storing data in a full void space', async () => {
    qvge.activate();
    const voidId = await qvge.generateVoidSpace('Mars Orbit', 1024);
    const data = { size: 2048 }; // Exceeding the capacity

    await expect(qvge.storeInVoid(voidId, data)).rejects.toThrow('Void space full');
  });

  test('should throw an error when trying to store data in a non-existent void space', async () => {
    const data = { size: 1024 };
    await expect(qvge.storeInVoid('non-existent-void', data)).rejects.toThrow('Void space not found');
  });

  test('should list all void spaces', async () => {
    qvge.activate();
    await qvge.generateVoidSpace('Mars Orbit', 1e21);
    await qvge.generateVoidSpace('Asteroid Belt', 1e21);

    const voidSpaces = await qvge.listVoidSpaces();
    expect(voidSpaces.length).toBe(2);
    expect(voidSpaces[0]).toHaveProperty('location', 'Mars Orbit');
    expect(voidSpaces[1]).toHaveProperty('location', 'Asteroid Belt');
  });

  test('should clear a void space successfully', async () => {
    qvge.activate();
    const voidId = await qvge.generateVoidSpace('Mars Orbit', 1e21);
    const data = { size: 1024 };

    await qvge.storeInVoid(voidId, data);
    await qvge.clearVoidSpace(voidId);
    expect(qvge.voidSpaces.get(voidId).used).toBe(0);
  });

  test('should throw an error when clearing a non-existent void space', async () => {
    await expect(qvge.clearVoidSpace('non-existent-void')).rejects.toThrow('Void space not found');
  });

  afterEach(() => {
    qvge.deactivate(); // Deactivate the engine after each test
  });
});
