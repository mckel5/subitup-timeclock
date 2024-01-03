# SubItUp Timeclock

This repository contains an automated timeclock system that interfaces with SubItUp. It is designed to run on a Raspberry Pi or other microcomputer with an I2C character LCD screen and a magstripe card reader attached. Users swipe their ID card and the program either clocks them in or out, reporting the status of the operation on the LCD screen.

## Setup

Before running the program, you must clock in/out normally using the SubItUp web interface and grab some information from the HTTP requests. These values should be saved in `consts.py`:

* `eid` (int)
* `deviceKey` (str)
* `deviceSecret` (str)
* `deviceUniqueID` (str)
* `deptkey` (str)

You must also create a `users.py` file containing a dictionary that maps user IDs (str) to names (str). This is for display purposes on the LCD screen only.

Finally, install all of the required modules listed in `requirements.txt`.

## Running

To run the program, run `python main.py`.