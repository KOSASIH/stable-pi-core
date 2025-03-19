// stable-pi-core/self-healing/gossip-protocol/gossipNode.js

const dgram = require('dgram'); // For UDP communication
const EventEmitter = require('events'); // For event handling
const winston = require('winston'); // For logging
const os = require('os');

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'gossipNode.log' }),
        new winston.transports.Console()
    ]
});

class GossipNode extends EventEmitter {
    constructor(port) {
        super();
        this.port = port;
        this.address = this.getLocalAddress();
        this.peers = new Set(); // Set to store peer addresses
        this.server = dgram.createSocket('udp4');

        this.server.on('message', (msg, rinfo) => {
            this.handleMessage(msg, rinfo);
        });

        this.server.on('listening', () => {
            const address = this.server.address();
            logger.info(`Gossip node listening on ${address.address}:${address.port}`);
        });

        this.server.bind(this.port);
    }

    // Get the local address of the node
    getLocalAddress() {
        const interfaces = os.networkInterfaces();
        for (const iface in interfaces) {
            for (const addr of interfaces[iface]) {
                if (addr.family === 'IPv4' && !addr.internal) {
                    return addr.address;
                }
            }
        }
        throw new Error('No valid IPv4 address found');
    }

    // Broadcast a message to all peers
    broadcast(message) {
        const msgBuffer = Buffer.from(JSON.stringify(message));
        this.peers.forEach(peer => {
            this.server.send(msgBuffer, this.port, peer, (err) => {
                if (err) {
                    logger.error(`Error sending message to ${peer}: ${err.message}`);
                } else {
                    logger.info(`Message sent to ${peer}: ${JSON.stringify(message)}`);
                }
            });
        });
    }

    // Handle incoming messages
    handleMessage(msg, rinfo) {
        const message = JSON.parse(msg.toString());
        logger.info(`Received message from ${rinfo.address}:${rinfo.port}: ${JSON.stringify(message)}`);

        // Add the sender to the peers set
        this.peers.add(`${rinfo.address}:${rinfo.port}`);

        // Emit an event for further processing
        this.emit('message', message);
    }

    // Discover peers (this is a placeholder; implement your discovery logic)
    discoverPeers() {
        // Example: Send a discovery message to a known multicast address
        const discoveryMessage = { type: 'DISCOVERY', address: this.address };
        this.broadcast(discoveryMessage);
    }

    // Start the gossip protocol
    start() {
        logger.info('Starting gossip protocol...');
        this.discoverPeers();
    }
}

// Example usage
if (require.main === module) {
    const port = process.argv[2] || 8080; // Use provided port or default to 8080
    const gossipNode = new GossipNode(port);
    gossipNode.start();

    // Listen for messages
    gossipNode.on('message', (message) => {
        // Handle the received message (e.g., update state, trigger actions)
        logger.info(`Processing received message: ${JSON.stringify(message)}`);
    });
}

module.exports = GossipNode;
