import time
import neopixel
import digitalio
import busio
import board

# Set up NeoPixel strip
num_pixels = 8
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = 0.12

BLACK = (0, 0, 0) 
RED = (250, 0, 0)  # color to blink
GREEN = (0, 250, 0)
BLUE = (0, 0, 250)
WHITE = (255, 255, 255)
pixels[0] = BLACK

pixels[1] = BLACK
pixels[2] = BLACK
pixels[3] = BLACK
pixels[4] = BLACK
pixels[5] = BLACK
pixels[6] = BLACK
pixels[7] = BLACK
pixels.show()
# Set up Serial
uart = busio.UART(board.GP8, board.GP9, baudrate=9600)
uart.write("Ws2812 Control".encode('utf-8'))

while True:
    if uart.in_waiting > 0:
        
        received_data = uart.readline().decode().strip()
        lenWS=len(received_data)

        if lenWS>= 55 : 
            colors = received_data.split(",")
 
            for i, color in enumerate(colors):
                r = int(color[0:2], 16)  # RED
                g = int(color[2:4], 16)  # GREEN
                b = int(color[4:6], 16)  # BLUE
                pixels[i] = (r, g, b)  #  NeoPixel 
                
            pixels.show()



