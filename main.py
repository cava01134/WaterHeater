import network
import espnow
from machine import Pin, ADC
import math
import time
import uasyncio as asyncio

adc = ADC(Pin(2, Pin.IN))
relay =  Pin(4, Pin.OUT)
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
wlan_mac = wlan_sta.config('mac')
print("MASTER_MAC:", wlan_mac) # Current Device Mac Address

# Initiate ESPNow
e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # Enter MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()
e.send(peer, "Starting...")


def read_ntc_temperature(x):
    x = adc.read_u16() # Read the raw analog value
    temperature = 1 / (math.log(1/(65535/x - 1))/ 3850 + 1/298.15) - 273.15
    return temperature

async def temperature_monitor():
    while True:
        temperature = read_ntc_temperature(x)
        print("Temperature: {:.2f} °C".format(temperature))
        if temperature <= 75:
            relay.value(1)
            elif temperature >= 73:
                relay.value(0)
        e.send(peer, str(temperature))
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.create_task(temperature_monitor())
loop.run_forever()