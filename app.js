// SolMate dashboard, Week 1: read-only view of telemetry over MQTT WebSockets.
const PREFIX = 'solmate/unit1';
const BROKER_URL = 'ws://localhost:9001';   // Week 1 local test; cloud wss:// comes in Week 2
const OFFLINE_AFTER_MS = 10000;             // no telemetry for 10 s = device offline

const $ = (id) => document.getElementById(id);
let lastSeen = 0;

const client = mqtt.connect(BROKER_URL, {
  clientId: 'web-' + Math.random().toString(16).slice(2),
  reconnectPeriod: 3000,
});

client.on('connect', () => {
  setBroker('Connected', true);
  client.subscribe(`${PREFIX}/#`);
});
client.on('reconnect', () => setBroker('Reconnecting...', false));
client.on('close', () => setBroker('Disconnected', false));

client.on('message', (topic, payload) => {
  const text = payload.toString();

  if (topic === `${PREFIX}/telemetry`) {
    let d;
    try { d = JSON.parse(text); } catch { return; }   // ignore bad messages
    lastSeen = Date.now();
    showTelemetry(d);
    setDevice(true);
  }

  if (topic === `${PREFIX}/status`) {
    setDevice(text === 'online');
  }
});

function showTelemetry(d) {
  set('power', d.power_w);
  set('voltage', d.voltage_v);
  set('current', d.current_a);
  set('az', d.az_deg);
  set('el', d.el_deg);
  set('imu', d.imu_pitch_deg);
  set('mode', d.mode);
  set('temp', d.temp_c);
  set('last', new Date().toLocaleTimeString());
  $('badge').classList.toggle('hidden', d.source !== 'simulator');
}

function set(id, value) {
  $(id).textContent = (value === undefined || value === null) ? '--' : value;
}

function setBroker(text, ok) {
  $('broker').textContent = text;
  $('broker').className = ok ? 'online' : 'offline';
}

function setDevice(online) {
  $('device').textContent = online ? 'Online' : 'Offline';
  $('device').className = online ? 'online' : 'offline';
}

// Watchdog: if telemetry stops, show the device as offline
setInterval(() => {
  if (lastSeen && Date.now() - lastSeen > OFFLINE_AFTER_MS) setDevice(false);
}, 1000);
