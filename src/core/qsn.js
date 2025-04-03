const { tcp } = require('../quantum/tcp');
const { srnf } = require('../space/srnf');

class QuantumSingularityNexus {
  constructor() {
    this.active = false;
    this.connectedNodes = new Set();
  }

  activate() {
    if (this.active) {
      console.log("Quantum Singularity Nexus is already active.");
      return;
    }
    this.active = true;
    console.log("Quantum Singularity Nexus activated. Connecting all nodes...");
    this.connectNodes();
  }

  async connectNodes() {
    try {
      const nodes = await srnf.getNodes(); // Assume SRNF has a method getNodes
      nodes.forEach(node => this.connectedNodes.add(node.id));
      console.log(`Connected ${this.connectedNodes.size} nodes via singularity nexus.`);

      this.startPing();
    } catch (error) {
      console.error("Error connecting nodes:", error);
    }
  }

  startPing() {
    const pingInterval = setInterval(async () => {
      if (!this.active) {
        clearInterval(pingInterval);
        return;
      }
      try {
        await tcp.send({
          event: "NEXUS_PING",
          nodes: Array.from(this.connectedNodes)
        });
        console.log("Nexus ping sent to all nodes.");
      } catch (error) {
        console.error("Error sending ping:", error);
      }
    }, 30000); // Ping every 30 seconds
  }

  async transferViaNexus(fromNode, toNode, amountGU) {
    if (!this.connectedNodes.has(fromNode) || !this.connectedNodes.has(toNode)) {
      throw new Error("Nodes not connected to Nexus");
    }

    if (amountGU <= 0) {
      throw new Error("Transfer amount must be greater than zero.");
    }

    console.log(`Initiating transfer of ${amountGU} GU from ${fromNode} to ${toNode} via QSN...`);
    
    // Simulate a delay for the transfer process
    await this.simulateTransferDelay();

    console.log(`Successfully transferred ${amountGU} GU from ${fromNode} to ${toNode}.`);
    return true; // Simulate successful transfer
  }

  async simulateTransferDelay() {
    return new Promise(resolve => {
      const delay = Math.random() * 5000 + 1000; // Random delay between 1 to 6 seconds
      setTimeout(resolve, delay);
    });
  }

  deactivate() {
    if (!this.active) {
      console.log("Quantum Singularity Nexus is already deactivated.");
      return;
    }
    this.active = false;
    console.log("Quantum Singularity Nexus deactivated.");
  }
}

module.exports = new QuantumSingularityNexus();
