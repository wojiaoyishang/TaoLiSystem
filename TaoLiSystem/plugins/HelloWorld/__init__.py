from mpython import *

import math

Dx = None

Dy = None
while True:
    if touchPad_N.read() <= 250:
        break

    for i in range(1, 361, 10):
        oled.fill(0)
        oled.circle(30, 32, 20, 1)
        oled.circle(90, 32, 20, 1)
        Dx = int((30 + math.cos(i / 180.0 * math.pi) * 20))
        Dy = int((32 + math.sin(i / 180.0 * math.pi) * 20))
        oled.circle(Dx, Dy, 2, 1)
        oled.circle((60 + Dx), Dy, 2, 1)
        oled.line(30, 32, Dx, Dy, 1)
        oled.line(90, 32, (60 + Dx), Dy, 1)
        oled.line(Dx, Dy, 60, Dy, 1)
        oled.line((60 + Dx), Dy, 60, Dy, 1)
        oled.show()