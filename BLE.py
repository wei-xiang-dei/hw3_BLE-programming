from bluepy.btle import Scanner, DefaultDelegate
from bluepy.btle import Peripheral, UUID, Descriptor


class MyDelegate (DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif (isNewData):
            print("Received new data from", dev.addr)

    def handleNotification(self, cHandle, data):
        print("Received notification: %s" % data)


scanner = Scanner().withDelegate(MyDelegate())
devices = scanner.scan(10.0)
n = 0
for dev in devices:
    print("%d: Device %s (%s), RSSI=%d dB" %
          (n, dev.addr, dev.addrType, dev.rssi))
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print(" %s = %s" % (desc, value))
number = int(input('Enter your device number: '))
print('Device', number)
print(list(devices)[number].addr)
print("Connecting...")
dev = Peripheral(list(devices)[number].addr, 'public')
print("Services...")
for svc in dev.services:
    print(str(svc))
try:
    testService = dev.getServiceByUUID(UUID(0xfff0))
    for ch in testService.getCharacteristics():
        print(str(ch))
    ch = dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    if (ch.supportsRead()):
        print(ch.read().decode('UTF-8'))
    ch1 = dev.getCharacteristics(uuid=UUID(0xfff2))[0]
    des = ch1.getDescriptors(forUUID=0x2902)[0]
    print(des.read())
    setup_data = b'\x01\x00'
    des.write(setup_data, True)
    print("Notifiying Enabled")
finally:
    dev.disconnect()
