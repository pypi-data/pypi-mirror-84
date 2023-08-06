from RPLCD.i2c import CharLCD, BaseCharLCD
import logging


class Lcd:

    @staticmethod
    def createI2C(i2c_expander: str, i2c_address: int) -> BaseCharLCD:
        logging.info("bind driver to address " + hex(i2c_address) + " using port expander " + i2c_expander)
        return CharLCD(i2c_expander, i2c_address)

    def __init__(self, char_lcd: BaseCharLCD, num_lines: int, num_chars_per_line: int):
        self.char_lcd = char_lcd
        self.num_lines = num_lines
        self.num_chars_per_line = num_chars_per_line

    def write(self, text):
        logging.debug("writing text: " + text)
        self.char_lcd.clear()
        self.char_lcd.write_string(text)