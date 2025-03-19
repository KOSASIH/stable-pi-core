// stable-pi-core/self-healing/ai-security/dataCollector.js

const fs = require('fs');
const os = require('os');
const path = require('path');
const winston = require('winston'); // For logging

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'dataCollector.log' }),
        new winston.transports.Console()
    ]
});

class DataCollector {
    constructor() {
        this.data = [];
        this.interval = 5000; // Collect data every 5 seconds
        this.outputFilePath = path.join(__dirname, 'collectedData.json');
    }

    // Collect system metrics
    collectMetrics() {
        const metrics = {
            timestamp: new Date().toISOString(),
            cpuUsage: this.getCpuUsage(),
            memoryUsage: this.getMemoryUsage(),
            networkInterfaces: this.getNetworkInterfaces(),
            loadAverage: os.loadavg(),
        };

        this.data.push(metrics);
        logger.info('Collected metrics:', metrics);
    }

    // Get CPU usage
    getCpuUsage() {
        const cpus = os.cpus();
        const total = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b, 0), 0);
        const idle = cpus.reduce((acc, cpu) => acc + cpu.times.idle, 0);
        return ((total - idle) / total) * 100; // CPU usage percentage
    }

    // Get memory usage
    getMemoryUsage() {
        const totalMemory = os.totalmem();
        const freeMemory = os.freemem();
        return ((totalMemory - freeMemory) / totalMemory) * 100; // Memory usage percentage
    }

    // Get network interfaces information
    getNetworkInterfaces() {
        return os.networkInterfaces();
    }

    // Save collected data to a JSON file
    saveData() {
        try {
            fs.writeFileSync(this.outputFilePath, JSON.stringify(this.data, null, 2));
            logger.info('Collected data saved to:', this.outputFilePath);
        } catch (error) {
            logger.error('Error saving collected data:', error);
        }
    }

    // Start collecting data at regular intervals
    startCollecting() {
        this.collectMetrics(); // Initial collection
        this.intervalId = setInterval(() => {
            this.collectMetrics();
        }, this.interval);
    }

    // Stop collecting data
    stopCollecting() {
        clearInterval(this.intervalId);
        this.saveData();
    }
}

// Usage example
const dataCollector = new DataCollector();
dataCollector.startCollecting();

// Stop collecting after a certain period (e.g., 30 seconds for demonstration)
setTimeout(() => {
    dataCollector.stopCollecting();
}, 30000);

module.exports = DataCollector;
