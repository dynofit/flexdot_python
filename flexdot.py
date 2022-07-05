import asyncio
import sys
from matplotlib.pyplot import *
from bleak import BleakScanner, BleakClient
import decompress

dots = []

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print("Found: ", d)

        if d.name == "Dynofit Inc Flexdot":
            print("Found a flexdot")
            dots.append(d.address)

asyncio.run(main())

if len(dots) != 1:
    print("Did not find exactly one dot :( ")
    sys.exit(1)

print(f"Connecting to {dots[0]}")

_emg_envelope = "e5f49879-6ee1-479e-bfec-3d35e13d3b88"
_emg_raw = "001785a0-cf2e-47f5-9d43-1217696f8ef9"


emg_signal = []
history=500
f = figure()

def notification_handler(sender, data):
    print("{0}: {1}".format(sender, data))
    print(len(data))
    
    return
    global emg_signal
    emg_signal+=data
    if len(emg_signal) > history:
        emg_signal = emg_signal[-history:]
    
    clf()
    plot(emg_signal)
    draw()
    show(block=False)
    f.canvas.flush_events()




async def set_notifications(address, char_uuid, callback):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
            
        while True:
            await client.start_notify(char_uuid, callback)

asyncio.run(set_notifications(dots[0], _emg_raw, notification_handler))
