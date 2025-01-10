import audiomp3
import audiobusio
import busio
import board
import digitalio
import time
import displayio
import random
import terminalio
from adafruit_displayio_ssd1306 import SSD1306

# Define I2S pins on Raspberry Pi Pico
bit_clock_pin = board.GP16  # BCK (Bit Clock) pin
word_select_pin = board.GP17  # WS or LRCK (Word Select) pin
data_pin = board.GP18  # DATA pin

# Initialize I2SOut
audio = audiobusio.I2SOut(bit_clock=bit_clock_pin, word_select=word_select_pin, data=data_pin)

# Set GP1 as output for controlling XSMT (Soft Mute)
xsmt_pin = digitalio.DigitalInOut(board.GP1)
xsmt_pin.direction = digitalio.Direction.OUTPUT

# Create a list of MP3 filenames
mp3_files = ["YakT.mp3", "YakE.mp3", "Testrp2040.mp3", "e1.mp3", "e2.mp3", "e3.mp3"]

# Display setup
displayio.release_displays()

SDA = board.GP8
SCL = board.GP9
i2c = busio.I2C(SCL, SDA)

display_bus = displayio.I2CDisplay(i2c, device_address=60)
display = SSD1306(display_bus, width=128, height=32)

# Constants
WIDTH = 128
HEIGHT = 32
BAR_WIDTH = 8
MAX_BAR_HEIGHT = 28
NUM_BARS = (WIDTH - 32) // BAR_WIDTH  # Adjust for icon

# Create the display group
splash = displayio.Group()
display.show(splash)

icon_file = "/spk.bmp"  # Path to your BMP file
icon_bitmap = displayio.OnDiskBitmap(open(icon_file, "rb"))
icon_tile = displayio.TileGrid(icon_bitmap, pixel_shader=icon_bitmap.pixel_shader, x=0, y=0)
splash.append(icon_tile)

# Create and initialize bars
bars = []
for i in range(NUM_BARS):
    bar_bitmap = displayio.Bitmap(BAR_WIDTH, MAX_BAR_HEIGHT, 2)
    bar_palette = displayio.Palette(2)
    bar_palette[0] = 0x000000  # Background color (Black)
    bar_palette[1] = 0xFFFFFF  # Foreground color (White)
    bar_sprite = displayio.TileGrid(bar_bitmap, pixel_shader=bar_palette, x=32 + i * BAR_WIDTH, y=0)
    bars.append(bar_sprite)
    splash.append(bar_sprite)

# Function to update bars
def update_bars():
    for i, bar in enumerate(bars):
        bar_height = random.randint(1, MAX_BAR_HEIGHT)  # Random height for each bar
        for x in range(BAR_WIDTH):
            for y in range(MAX_BAR_HEIGHT):
                if y < bar_height:
                    bar.bitmap[x, MAX_BAR_HEIGHT - y - 1] = 1  # Draw bar
                else:
                    bar.bitmap[x, MAX_BAR_HEIGHT - y - 1] = 0  # Clear remaining space

# Main loop
while True:
    for mp3_file_name in mp3_files:
        # Open the MP3 file
        with open(mp3_file_name, "rb") as mp3_file:
            # Create an MP3Decoder object
            decoder = audiomp3.MP3Decoder(mp3_file)

            # Unmute before playing the song
            print(f"Unmute and start playing: {mp3_file_name}")
            xsmt_pin.value = True  # Unmute XSMT

            # Play the audio
            audio.play(decoder)

            # Wait until the song finishes playing
            while audio.playing:
                update_bars()  # Update the graph bars while the song is playing
                display.refresh()  # Force refresh the display
                time.sleep(0.05)

            print("Song playback finished!")

            # Mute after the song finishes
            xsmt_pin.value = False  # Mute XSMT

            # Wait for 5 seconds before playing the next file
            time.sleep(5)
