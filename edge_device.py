import socket
import paho.mqtt.client as mqtt

# MQTT settings
broker = "broker.emqx.io"
topic = "savonia/iot/temperature"

# Socket settings
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 5000

# Setup MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(broker, 1883)
print(f"Connected to MQTT broker: {broker}")

# Setup Socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Socket server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected by sensor at {addr}")
    
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            print(f"Received from sensor: {data}")
            
            # Publish to MQTT
            mqtt_client.publish(topic, data)
            print(f"Published to MQTT topic '{topic}': {data}")
            
    except ConnectionResetError:
        print("Sensor disconnected.")
    finally:
        conn.close()
        print("Waiting for new connection...")
