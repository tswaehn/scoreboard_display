import time
import board
import neopixel
from wifi_connect import connect_wifi, http_get_test

# 1 NeoPixel on the board
pixel = neopixel.NeoPixel(
    board.NEOPIXEL,  # pin
    1,               # number of pixels
    brightness=0.01,  # 0.0 - 1.0
    auto_write=True  # update immediately when we assign
)

while True:
    for i in range(3):
        pixel[0] = (255, 255, 255)
        time.sleep(0.2)
        pixel[0] = (0, 255, 0)
        time.sleep(0.2)
        pixel[0] = (0, 0, 255)
        time.sleep(0.2)

    pixel[0] = (255, 0, 0)

    print("Booting MatrixPortal WiFi test...")

    while True:
        if not connect_wifi():
            print("WiFi connection failed, stopping.")
        else:
            break

    print("Done. Looping every 30s.")
    while True:
        pixel[0] = (0, 255, 255)

        if http_get_test():
            # ok
            pixel[0] = (0, 0, 255)
        else:
            pixel[0] = (255, 0, 255)

        time.sleep(10)
