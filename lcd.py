import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from time import sleep
from CircuitPython_LCD.lcd.lcd import LCD
from CircuitPython_LCD.lcd.i2c_pcf8574_interface import I2CPCF8574Interface

def init() -> LCD:
    i2c = busio.I2C(board.SCL, board.SDA)
    cols = 20
    rows = 4
    address = 0x27
    return LCD(I2CPCF8574Interface(i2c, address), num_rows=rows, num_cols=cols)

