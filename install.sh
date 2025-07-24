#!/bin/bash

set -e

SERVICE_NAME="mqtt-relay"
INSTALL_DIR="/opt/mqtt-relay"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

echo "📦 Installing MQTT Relay service..."

# Create install directory
sudo mkdir -p "$INSTALL_DIR"
sudo cp mqtt_relay.py "$INSTALL_DIR"
sudo chmod +x "$INSTALL_DIR/mqtt_relay.py"

# Create systemd service file
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=MQTT GPIO Relay Controller
After=network.target

[Service]
ExecStart=/usr/bin/python3 $INSTALL_DIR/mqtt_relay.py
WorkingDirectory=$INSTALL_DIR
StandardOutput=journal
StandardError=journal
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOF

# Reload and enable service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

echo "✅ Service '$SERVICE_NAME' installed and started."
