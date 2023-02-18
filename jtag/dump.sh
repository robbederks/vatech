#!/bin/bash -e

openocd -d -f vatech.cfg -c "init;" -c "flash read_bank 0 firmware.bin 0 0x400000" -c "exit"