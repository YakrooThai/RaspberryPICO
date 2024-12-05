import time
import board
import busio
import adafruit_vl53l0x
from adafruit_st7735 import ST7735R
import displayio
import terminalio
from adafruit_display_text import label
import digitalio

# Setup I2C for the VL53L0X distance sensor
SDA = board.GP14
SCL = board.GP15
i2c = busio.I2C(SCL, SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# Release any previously configured displays
displayio.release_displays()

# Setup for the ST7735 display
mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP19
dc_pin = board.GP16

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin, baudrate=31250000)
display = ST7735R(display_bus, width=160, height=128, bgr=True, rotation=270)

# Create a display group
splash = displayio.Group()
display.root_group = splash  # Set the display group as the root for rendering

# Display the first line of text "YAKROO108" at the top
text_area_1 = label.Label(terminalio.FONT, text="YAKROO108", color=0xFFFFFF, x=10, y=20)  # Adjust x and y for position
splash.append(text_area_1)

# Display the second line of text "Distance : xx mm" (initially empty)
text_area_2 = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=10, y=50)  # Adjust x and y for position
splash.append(text_area_2)

# Main loop to read distance and update the display
while True:
    # Read distance from the sensor
    distance = vl53.range
    print("Range: {0}mm".format(distance))

    # Update the second line with the distance value
    text_area_2.text = "Distance : {0} mm".format(distance)

    # Wait for one second
    time.sleep(1.0)
