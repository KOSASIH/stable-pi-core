# MQTT Configuration Settings

mqtt:
  broker: "mqtt.example.com"  # Replace with your MQTT broker address
  port: 1883                   # Default MQTT port
  keep_alive: 60               # Keep alive interval in seconds
  client_id: "device123"       # Unique client ID for the MQTT client
  username: "your_username"    # MQTT username (if required)
  password: "your_password"     # MQTT password (if required)
  clean_session: true           # Whether to start with a clean session
  will:
    topic: "iot/devices/device123/status"  # Last Will and Testament topic
    message: "Device disconnected"          # Last Will and Testament message
    qos: 1                                  # QoS level for the Last Will message
    retain: false                           # Retain flag for the Last Will message
  topic:
    publish: "iot/devices/device123/data"  # Topic for publishing data
    subscribe: "iot/devices/device123/commands"  # Topic for subscribing to commands
