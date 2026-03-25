import paho.mqtt.client as mqtt
import requests

broker = "broker.emqx.io"
topic = "savonia/iot/temperature"

TOKEN = "8732626680:AAGbYwtuMc7YWFKOKbdjfCDX7p05IEiKdmY"
CHAT_ID = "1628845184"

threshold = 28

def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker!")
        client.subscribe(topic)
    else:
        print("Connection failed, code:", rc)

def on_message(client, userdata, msg):

    temperature = float(msg.payload.decode())

    print("Temperature:", temperature)

    if temperature > threshold:

        alert = f"ALERT: High temperature {temperature} °C"

        print(alert)

        send_telegram(alert)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883)

client.loop_forever()