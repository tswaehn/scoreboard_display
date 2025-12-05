import time
import ssl
import wifi
import socketpool
import adafruit_requests

# ----- CONFIG: change these -----
WIFI_SSID = "failed to connect"
WIFI_PASSWORD = "5highe7u"

TEST_URL = "https://httpbin.org/get"
# or any other URL, e.g. "https://example.com"
# -------------------------------


def connect_wifi():
    print("Connecting to WiFi:", WIFI_SSID)
    try:
        wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    except Exception as e:
        print("WiFi connect failed:", e)
        return False

    # wait for IP
    t0 = time.monotonic()
    while not wifi.radio.ipv4_address:
        if time.monotonic() - t0 > 15:
            print("Timeout waiting for IP address")
            return False
        time.sleep(0.5)

    print("Connected, IP:", wifi.radio.ipv4_address)
    return True


def http_get_test():
    print("Creating socket pool...")
    pool = socketpool.SocketPool(wifi.radio)
    print("Creating SSL context...")
    context = ssl.create_default_context()
    print("Creating requests session...")
    requests = adafruit_requests.Session(pool, context)

    print("Sending GET to:", TEST_URL)
    try:
        response = requests.get(TEST_URL)
        print("Status:", response.status_code)
        print("Headers:", response.headers)
        print("Body:")
        print(response.text)
        response.close()
    except Exception as e:
        print("HTTP request failed:", e)

