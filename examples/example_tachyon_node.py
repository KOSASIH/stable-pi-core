# examples/example_tachyon_node.py

import asyncio
from tcp.tachyon_node import TachyonNode
from tcp.data_packet import DataPacket

async def main():
    # Create two Tachyon Nodes
    sender_node = TachyonNode("SenderNode", "localhost:8000", None)
    receiver_node = TachyonNode("ReceiverNode", "localhost:8001", None)

    # Simulate sending a data packet
    data_packet = DataPacket(sender_node.node_id, receiver_node.node_id, {"message": "Hello, Receiver!"})
    
    print(f"{sender_node.node_id} is sending data...")
    await sender_node.send_data(receiver_node, data_packet)

    # Simulate receiving data
    print(f"{receiver_node.node_id} is ready to receive data.")
    await receiver_node.handle_received_data(data_packet)

if __name__ == "__main__":
    asyncio.run(main())
