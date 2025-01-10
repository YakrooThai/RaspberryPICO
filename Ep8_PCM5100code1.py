import audiomp3
import audiobusio
import board
import digitalio
import time

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
                pass

            print("Song playback finished!")

            # Mute after the song finishes
            xsmt_pin.value = False  # Mute XSMT

            # Wait for 5 seconds before playing the next file
            time.sleep(5)
