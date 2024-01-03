import lcd as lcd_mod
from users import users
from timeclock import is_clocked_in, clock_in, clock_out
from time import sleep
import logging
from datetime import datetime

logging.basicConfig(
    filename="log.txt",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)

MSG_DISPLAY_TIME = 5

def main():
    lcd = lcd_mod.init()

    # Input loop
    while True:
        lcd.clear()
        lcd.print("Waiting for swipe...")
        employee_id = input()

        lcd.clear()
        
        if len(employee_id) != 9 or employee_id not in users.keys():
            lcd.print(f"Invalid ID:\n{employee_id}")
            sleep(MSG_DISPLAY_TIME)
            continue

        try:
            name = users[employee_id]

            if is_clocked_in(employee_id):
                clock_out(employee_id)
                lcd.print(f"Clocked out\n{name}")
            else:
                clock_in(employee_id)
                lcd.print(f"Clocked in\n{name}")
            
            lcd.print("\n")
            lcd.print(datetime.now().strftime("%a. %b. %d, %Y\n%I:%M %p"))
            sleep(MSG_DISPLAY_TIME)

        except Exception as e:
            lcd.print("Error! :(\nSee log for details")
            logging.exception("Exception occurred")
            sleep(MSG_DISPLAY_TIME)
            continue

if __name__ == "__main__":
    main()
