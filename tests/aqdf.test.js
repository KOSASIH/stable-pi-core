// tests/aqdf.test.js
const AstroQuantumDestinyForge = require('./aqdf');

describe('AstroQuantumDestinyForge Tests', () => {
  beforeEach(() => {
    // Reset the instance before each test
    AstroQuantumDestinyForge.timelines = [];
  });

  test('should simulate a timeline with events', async () => {
    const events = [
      { name: "Galactic Trade Agreement", successThreshold: 0.7 },
      { name: "Interstellar Exploration Mission", successThreshold: 0.5 },
    ];

    const outcomes = await AstroQuantumDestinyForge.simulateTimeline(events);
    expect(outcomes.length).toBe(events.length);
    outcomes.forEach((outcome, index) => {
      expect(outcome.event).toBe(events[index].name);
      expect(['Success', 'Failure']).toContain(outcome.outcome);
      expect(outcome.probability).toBeGreaterThanOrEqual(0);
      expect(outcome.probability).toBeLessThan(1);
    });
  });

  test('should evaluate event outcomes correctly', () => {
    const event = { name: "Test Event", successThreshold: 0.5 };
    const successOutcome = AstroQuantumDestinyForge.evaluateEvent(event, 0.6);
    const failureOutcome = AstroQuantumDestinyForge.evaluateEvent(event, 0.4);
    
    expect(successOutcome).toBe("Success");
    expect(failureOutcome).toBe("Failure");
  });

  test('should store simulated timelines', async () => {
    const events = [
      { name: "Galactic Trade Agreement", successThreshold: 0.7 },
    ];

    await AstroQuantumDestinyForge.simulateTimeline(events);
    expect(AstroQuantumDestinyForge.timelines.length).toBe(1);
  });

  test('should retrieve the last simulated timeline', async () => {
    const events = [
      { name: "Galactic Trade Agreement", successThreshold: 0.7 },
    ];

    await AstroQuantumDestinyForge.simulateTimeline(events);
    const lastTimeline = AstroQuantumDestinyForge.getLastTimeline();
    expect(lastTimeline.length).toBe(events.length);
    expect(lastTimeline[0].event).toBe(events[0].name);
  });

  test('should throw error when retrieving last timeline if none exist', () => {
    expect(() => AstroQuantumDestinyForge.getLastTimeline()).toThrow("No timelines have been simulated yet.");
  });

  test('should predict future events based on past timelines', async () => {
    const events = [
      { name: "Galactic Trade Agreement", successThreshold: 0.7 },
      { name: "Interstellar Exploration Mission", successThreshold: 0.5 },
    ];

    await AstroQuantumDestinyForge.simulateTimeline(events);
    await AstroQuantumDestinyForge.simulateTimeline(events); // Simulate again for more data

    const predictions = await AstroQuantumDestinyForge.predictFutureEvents();
    expect(predictions.length).toBe(2); // Should match the number of timelines simulated
    predictions.forEach(prediction => {
      expect(prediction.successRate).toBeGreaterThanOrEqual(0);
      expect(prediction.failureRate).toBeGreaterThanOrEqual(0);
      expect(prediction.successRate + prediction.failureRate).toBe(1); // Success + Failure should equal 1
    });
  });

  test('should throw error when predicting future events if no timelines exist', async () => {
    await expect(AstroQuantumDestinyForge.predictFutureEvents()).rejects.toThrow("No timelines available for prediction.");
  });

  test('should simulate a specific event correctly', async () => {
    const event = { name: "Cosmic Energy Harvest", successThreshold: 0.6 };
    const outcome = await AstroQuantumDestinyForge.simulateEvent(event);
    
    expect(outcome.event).toBe(event.name);
    expect(['Success', 'Failure']).toContain(outcome.outcome);
    expect(outcome.probability).toBeGreaterThanOrEqual(0);
    expect(outcome.probability).toBeLessThan(1);
  });
});
