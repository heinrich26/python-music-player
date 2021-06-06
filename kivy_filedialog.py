from time import sleep
from jnius import autoclass

Hardware = autoclass('org.renpy.android.Hardware')
print('DPI is', Hardware.getDPI())

Hardware.accelerometerEnable(True)
for x in xrange(20):
    print(Hardware.accelerometerReading())
    sleep(.1)
