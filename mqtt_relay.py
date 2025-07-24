# mqtt_relay.py
# MQTT-based GPIO Relay Control with Home Assistant Discovery

import paho.mqtt.client as mqtt
import gpiod
import time
import json

# MQTT Login credentials
mqtt_username = 'mqtt'
mqtt_password = 'xxxxxx'

# Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_CONTROL = "relays/control/#"
MQTT_TOPIC_STATE_BASE = "relays/state"

# BCM GPIO numbers of the relays
RELAY_PINS = [5, 6, 13, 16, 19, 20, 21, 26]

# GPIO setup
chip = gpiod.Chip("gpiochip0")
relay_lines = []

for pin in RELAY_PINS:
    line = chip.get_line(pin)
    line.request(consumer="mqtt-relay", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[1])
    relay_lines.append(line)

def get_relay_states():
    return [0 if line.get_value() == 0 else 1 for line in relay_lines]

def publish_states(client):
    states = get_relay_states()
    for i, state in enumerate(states):
        client.publish(f"{MQTT_TOPIC_STATE_BASE}/{i}", "on" if state == 0 else "off", retain=True)

    if all(state == 0 for state in states):
        all_state = "on"
    elif all(state == 1 for state in states):
        all_state = "off"
    else:
        all_state = "mixed"
    client.publish(f"{MQTT_TOPIC_STATE_BASE}/all", all_state, retain=True)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code:", rc)
    client.subscribe(MQTT_TOPIC_CONTROL)
    publish_discovery_config(client)
    publish_states(client)

def on_message(client, userdata, msg):
    try:
        print(f"Message received: {msg.topic} -> {msg.payload.decode()}")
        parts = msg.topic.split("/")
        if len(parts) == 3 and parts[1] == "control":
            target = parts[2]
            payload = msg.payload.decode().strip().lower()

            if payload in ["on", "1"]:
                value = 0
            elif payload in ["off", "0"]:
                value = 1
            else:
                print("Invalid payload")
                return

            if target == "all":
                for line in relay_lines:
                    line.set_value(value)
            else:
                index = int(target)
                if 0 <= index < len(relay_lines):
                    relay_lines[index].set_value(value)
                else:
                    print("Invalid relay index")

            publish_states(client)

    except Exception as e:
        print("Error handling message:", e)

def publish_discovery_config(client):
    for i, pin in enumerate(RELAY_PINS):
        unique_id = f"relay_{i}"
        base_topic = f"homeassistant/switch/{unique_id}"
        config = {
            "name": f"Relay {i}",
            "unique_id": unique_id,
            "state_topic": f"{MQTT_TOPIC_STATE_BASE}/{i}",
            "command_topic": f"relays/control/{i}",
            "payload_on": "on",
            "payload_off": "off",
            "state_on": "on",
            "state_off": "off",
            "qos": 0,
            "retain": True
        }
        client.publish(f"{base_topic}/config", json.dumps(config), retain=True)

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
