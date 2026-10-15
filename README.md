# SolMate App (Week 1)

Start here. Everything runs on your laptop for now.

## Run it

1. Start the broker:  `mosquitto -c mosquitto.conf -v`
2. Start the fake tracker in a second terminal:  `python3 sim/simulator.py`
3. Serve this folder in a third terminal:  `python3 -m http.server 8000`
4. Open `http://localhost:8000` in your browser.

You should see values change every 2 seconds, with a yellow SIMULATED DATA badge.

## Dummy values used by the simulator

| Value | Dummy range | Real source later |
|---|---|---|
| Voltage | 18.0 V ± 0.3 | INA219 |
| Current | Power / voltage | INA219 |
| Power | 0 to 300 W (daylight curve) | Calculated from INA219 |
| Azimuth | 120 to 240 degrees | Encoder or potentiometer |
| Elevation | 10 to 50 degrees | Encoder or potentiometer |
| IMU tilt | Elevation ± 0.5 degrees | MPU6050 (pitch) |
| Temperature | 29 to 31 °C | BME280 or MPU6050 |

## Notes

- The mqtt.js version in `index.html` is a starting value. If the link fails, check cdnjs for the latest 5.x and update it.
- The app is read-only in Week 1. Controls come in Week 2.
