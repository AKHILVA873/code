#!/bin/bash
/bin/sleep 5 && /usr/bin/python3 /home/dtrgenh1d1/code/shared_memory/triac_control.py
/bin/sleep 5 && /usr/bin/python3 /home/dtrgenh1d1/code/shared_memory/tacho_reader.py
/bin/sleep 5 && /usr/bin/python3 /home/dtrgenh1d1/code/shared_memory/adv_relay_control.py
/bin/sleep 5 && /usr/bin/python3 /home/dtrgenh1d1/code/shared_memory/sensor_reader.py
