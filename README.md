# 🟢 MQTT Relay Controller (Python + gpiod)

Useful tools for Waveshare RPi_Relay_Board_(B) , https://www.waveshare.com/wiki/RPi_Relay_Board_(B)

This Python script listens for MQTT messages on topics like `relays/control/#` and switches GPIO relays on a Raspberry Pi (or compatible Linux board) using the **`gpiod`** library.  
It also integrates with **Home Assistant** via MQTT discovery and publishes relay states to `relays/state/#`.

## ✅ Features

- Control up to 8 GPIO relays via MQTT
- Auto-discovery support for Home Assistant
- State feedback and `all`-relay control
- Works with `libgpiod` (not legacy RPi.GPIO)
- Secure MQTT credentials support

## 🧪 Dependencies

Ensure Python 3 and required libraries are installed:

```bash
sudo apt update
sudo apt install -y python3 python3-pip
sudo apt install -y python3-libgpiod
sudo apt install -y python3-paho-mqtt
pip3 install paho-mqtt gpiod
```

## 🛠️ Installation

```bash
[git clone https://github.com/your-username/mqtt-relay.git](https://github.com/thomas-ColumbaTek/Waveshare_RPi_Relay_Board_B.git)
cd Waveshare_RPi_Relay_Board_B/
chmod +x install.sh
./install.sh
```

## 🔍 Logs and Debugging

```bash
journalctl -u mqtt-relay -f
```

To restart the service:

```bash
sudo systemctl restart mqtt-relay
```

---
MIT License
