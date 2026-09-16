import network, urequests, time
from machine import Pin

WIFI_SSID = "home_ext"
WIFI_PASSWORD = "12345678"
BRIDGE_URL = "http://host.wokwi.internal:5000/sensor"

SENSORS = [
    (Pin(13, Pin.IN, Pin.PULL_UP), 9, "P009", "SENSOR_01"),
    (Pin(12, Pin.IN, Pin.PULL_UP), 10, "P010", "SENSOR_02"),
    (Pin(14, Pin.IN, Pin.PULL_UP), 11, "P011", "SENSOR_03"),
    (Pin(27, Pin.IN, Pin.PULL_UP), 12, "P012", "SENSOR_04"),
    (Pin(26, Pin.IN, Pin.PULL_UP), 13, "P013", "SENSOR_05"),
    (Pin(25, Pin.IN, Pin.PULL_UP), 14, "P014", "SENSOR_06"),
    (Pin(33, Pin.IN, Pin.PULL_UP), 15, "P015", "SENSOR_07"),
    (Pin(32, Pin.IN, Pin.PULL_UP), 16, "P016", "SENSOR_08"),
]

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.2)

def send(spot_id, code, source_id, occupied):
    payload = {"parkingSpotId": spot_id, "spotCode": code, "sourceId": source_id, "occupied": occupied}
    try:
        r = urequests.post(BRIDGE_URL, json=payload)
        r.close()
        print("sent", payload)
    except Exception as e:
        print("bridge error", e)

connect_wifi()
last = {}
while True:
    for pin, spot_id, code, source_id in SENSORS:
        occupied = pin.value() == 0
        if last.get(code) != occupied:
            send(spot_id, code, source_id, occupied)
            last[code] = occupied
    time.sleep(1)
