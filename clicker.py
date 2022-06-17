import time

import adbutils

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

devices = adb.device_list()

if len(devices) == 0:
    print('No devices')
    quit()

device = devices[0]

print(f'Connected to {device}')


while True:
    device.click(567, 935)
    time.sleep(0.2)
    device.click(567, 935)
    time.sleep(1.5)
    device.click(744, 1767)
    time.sleep(0.5)