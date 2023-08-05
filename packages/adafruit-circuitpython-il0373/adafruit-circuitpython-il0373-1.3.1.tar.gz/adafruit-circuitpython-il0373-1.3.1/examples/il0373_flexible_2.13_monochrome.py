"""Simple test script for 2.13" 212x104 monochrome display.

Supported products:
  * Adafruit Flexible 2.13" Monochrome
    * https://www.adafruit.com/product/4243
  """

import time
import board
import displayio
import adafruit_il0373

displayio.release_displays()

# This pinout works on a Feather M4 and may need to be altered for other boards.
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.D5
epd_busy = board.D6

display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
time.sleep(1)

display = adafruit_il0373.IL0373(
    display_bus, width=212, height=104, rotation=90, busy_pin=epd_busy, swap_rams=True
)

g = displayio.Group()

f = open("/display-ruler.bmp", "rb")

pic = displayio.OnDiskBitmap(f)
t = displayio.TileGrid(pic, pixel_shader=displayio.ColorConverter())
g.append(t)

display.show(g)

display.refresh()

time.sleep(120)
