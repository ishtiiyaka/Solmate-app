"""
SolMate fake tracker (Week 1).
Publishes DUMMY telemetry in the agreed topic format so the app can be built
before the real ESP32 is ready. Every message is marked source="simulator".
Stop with Ctrl+C.
"""
import json
import math
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
PREFIX = "solmate/unit1"
INTERVAL_S = 2

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Last-will: if this script dies, the broker publishes "offline" for us
client.will_set(f"{PREFIX}/status", "offline", qos=1, retain=True)
client.connect(BROKER, PORT, 60)
client.loop_start()
client.publish(f"{PREFIX}/status", "online", qos=1, retain=True)
print("Simulator running. Ctrl+C to stop.")

t = 0
try:
    while True:
        # Dummy daylight curve: 0 W at night, peaks at 300 W
        daylight = max(0.0, math.sin(t / 720))
        power = 300 * daylight + random.uniform(-5, 5)
        voltage = 18.0 + random.uniform(-0.3, 0.3)     # dummy panel voltage
        current = power / voltage if voltage else 0.0

        az = 180 + 60 * math.sin(t / 60)               # dummy azimuth sweep
        el = 30 + 20 * math.sin(t / 120)               # dummy elevation sweep

        payload = {
            "source": "simulator",
            "ts": int(time.time()),
            "mode": "auto",
            "az_deg": round(az, 1),
            "el_deg": round(el, 1),
            "az_target": 180.0,
            "el_target": 30.0,
            "power_w": round(power, 1),
            "voltage_v": round(voltage, 2),
            "current_a": round(current, 2),
            "imu_pitch_deg": round(el + random.uniform(-0.5, 0.5), 1),  # dummy MPU6050 reading
            "temp_c": round(30 + random.uniform(-1, 1), 1),
            "rssi": -60,
        }
        client.publish(f"{PREFIX}/telemetry", json.dumps(payload), qos=0)
        t += INTERVAL_S
        time.sleep(INTERVAL_S)
except KeyboardInterrupt:
    client.publish(f"{PREFIX}/status", "offline", qos=1, retain=True)
    client.loop_stop()
    client.disconnect()
    print("Simulator stopped.")
