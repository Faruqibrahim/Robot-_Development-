import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import time

def main():
    lcd_columns = 16 # How many characters we can fit on the screen
    lcd_rows = 2     # How many rows of characters we have

    # Replace x with the pin number, board.GPx in CircuitPython is the same as machine.Pin(x) in MicroPython
    scl_pin = board.GP5
    sda_pin = board.GP4

    i2c = busio.I2C(scl_pin, sda_pin)
    # Initialize the LCD
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
current_menu = "INITIAL"

while True:
    if current_menu == "INITIAL":
        if lcd.up_button:
            # Change the state
            current_menu = "VOLTAGE"
            # Clear screen
            lcd.clear()
            # Show voltage text
            lcd.message = getInputVoltage()

    elif current_menu == "VOLTAGE":
        if lcd.up_button:
            # Change the state
            current_menu = "INITIAL"
            # Clear screen
            lcd.clear()