import time
import threading
import requests
import json

from shared_memory_util import read_data_from_shared_memory, write_data_to_shared_memory

# Global variables to store shared memory values
door_status = None
triac_delay = None
taccosensor = None
water_level = None
command = 1000.0

# Shared memory names
shared_memory_names = [
    "relay_command",
    "taccosensor",
    "doorssensor",
    "Pressure",
    "Water_Level",
    "Door_Status",
    "triac_delay",
    "command_from_server"
]



# Function to update ready status
def update_ready(hubid, deviceid):
    # API URL
    url = "http://srv630050.hstgr.cloud:3000/api/users/updateReady"

    # JSON data to send in the request
    data = {
        "hubid": hubid,
        "deviceid": deviceid
    }

    try:
        # Make a POST request to the API
        response = requests.post(url, json=data)
    except Exception as e:
        dummy =1



# Function to update progress
def update_progress(hubid, deviceid, progress):
    # API URL
    url = "http://srv630050.hstgr.cloud:3000/api/users/updateProgress"

    # JSON data to send in the request
    data = {
        "hubid": hubid,
        "deviceid": deviceid,
        "progress": progress
    }

    try:
        # Make a POST request to the API
        response = requests.post(url, json=data)
    except Exception as e:
        dummy =1



def read_shared_memory():
    global door_status, triac_delay, taccosensor, water_level, command
    while True:
        try:
            # Read values from shared memory
            door_status = read_data_from_shared_memory("Door_Status")
            triac_delay = read_data_from_shared_memory("triac_delay")

            taccosensor = read_data_from_shared_memory("taccosensor")
            water_level = read_data_from_shared_memory("Pressure")
            command = read_data_from_shared_memory("command_from_server")
            dummy =1
            # taccosensor = read_data_from_shared_memory("taccosensor")
        except Exception as e:
            dummy =1
        time.sleep(1)  # Adjust the delay as needed


def close_door():
    # Close the door
    write_data_to_shared_memory("relay_command", 12.0)
    time.sleep(10)  # 100 milliseconds
    write_data_to_shared_memory("relay_command", 12.0)
    time.sleep(4)  # 100 milliseconds


def open_door():
    # Close the door
    write_data_to_shared_memory("relay_command", 12.0)
    time.sleep(4)  # 100 milliseconds
    # write_data_to_shared_memory("relay_command", 12.0)
    # time.sleep(4)  # 100 milliseconds
    # write_data_to_shared_memory("relay_command", 12.0)
    # time.sleep(4)  # 100 milliseconds



def drain_water(time_of_job):
    write_data_to_shared_memory("relay_command", 10.0)  # Turn on drain pump
    time.sleep(time_of_job)  # Wait for 10 seconds
    write_data_to_shared_memory("relay_command", 11.0)  # Turn off drain pump
    time.sleep(1)

def load_water(time_of_job):
    write_data_to_shared_memory("relay_command", 6.0)  # Turn on drain pump
    time.sleep(1)
    write_data_to_shared_memory("relay_command", 8.0)  # Turn on drain pump
    time.sleep(time_of_job)  # Wait for 10 seconds
    write_data_to_shared_memory("relay_command", 7.0)  # Turn off drain pump
    time.sleep(1)
    write_data_to_shared_memory("relay_command", 9.0)  # Turn off drain pump
    time.sleep(1)


def check_and_load_water(target_level):
    global door_status, triac_delay, taccosensor, water_level
    write_data_to_shared_memory("relay_command", 6.0)  # Turn on drain pump
    time.sleep(1)
    write_data_to_shared_memory("relay_command", 8.0)  # Turn on drain pump
    while (water_level>target_level):
        time.sleep(0.2)
    write_data_to_shared_memory("relay_command", 7.0)  # Turn off drain pump
    time.sleep(1)
    write_data_to_shared_memory("relay_command", 9.0)  # Turn off drain pump
    time.sleep(1)

def send_rpm(rpm_input):
    triac_delay = float(rpm_input)
    write_data_to_shared_memory("triac_delay", triac_delay)
    dummy =1

def rpm_leveler(required_rpm):
    global door_status, triac_delay, taccosensor, water_level
    req_rpm_input = triac_delay
    while(1):
        if((required_rpm-taccosensor)>=10):
            req_rpm_input=req_rpm_input-30
        elif((required_rpm-taccosensor)<=-10):
            req_rpm_input=req_rpm_input+30
        else:
            break
        send_rpm(req_rpm_input)
        time.sleep(1)


def stop_spin():
    write_data_to_shared_memory("relay_command", 5.0)
    time.sleep(5)  
    send_rpm(8000)
    dummy =1


def set_cl_direction():
    write_data_to_shared_memory("relay_command", 1.0)
    time.sleep(1)
    dummy =1


def set_al_direction():
    write_data_to_shared_memory("relay_command", 3.0)
    time.sleep(1)
    dummy =1


def drum_rotation_pattern_one():
    global door_status, triac_delay, taccosensor, water_level
    start_time = time.time()
    while(time.time() - start_time < 300):  # Run for 5 minutes (300 seconds)
        set_cl_direction()
        rpm_leveler(30)
        time.sleep(15)
        stop_spin()

        set_al_direction()
        rpm_leveler(30)
        time.sleep(15)
        stop_spin()
    dummy =1




def drum_rotation_pattern_two():
    global door_status, triac_delay, taccosensor, water_level
    start_time = time.time()
    while(time.time() - start_time < 300):  # Run for 5 minutes (300 seconds)
        set_cl_direction()
        rpm_leveler(40)
        time.sleep(15)
        stop_spin()

        set_al_direction()
        rpm_leveler(40)
        time.sleep(15)
        stop_spin()
    dummy =1


def cycle_end():
    write_data_to_shared_memory("relay_command", 14.0)  # Turn on drain pump


def door_control_procedure():
    global door_status, triac_delay, taccosensor, water_level, command
    start_flag =0

    while True:
        if command <=0.0:
            try:
                time.sleep(10)
                close_door()
                # Example usage
                update_progress("17348502838715973", 1000, "05")
                write_data_to_shared_memory("command_from_server", 05.0)
            except Exception as e:
                dummy =1
            



        elif command <=5.0:
            try:                    
                drain_water(10) # drain water for 10 seconds
                # load_water(50) # load water for 10 seconds

                # Example usage
                update_progress("17348502838715973", 1000, "10")
                write_data_to_shared_memory("command_from_server", 10.0)

            except Exception as e:
                dummy =1
            





        elif command <=10.0:
            try:                    
                check_and_load_water(13) # load water while reaching the level value less than 13
                # Example usage
                update_progress("17348502838715973", 1000, "15")
                write_data_to_shared_memory("command_from_server", 15.0)

            except Exception as e:
                dummy =1
            






        elif command <=15.0:
            try:                    
                send_rpm(8000)
                drum_rotation_pattern_one()
                # Example usage
                update_progress("17348502838715973", 1000, "20")
                write_data_to_shared_memory("command_from_server", 20.0)

            except Exception as e:
                dummy =1
            
            time.sleep(1)  # Adjust the delay as needed





        elif command <=20.0:
            try:                    
                check_and_load_water(13) # load water while reaching the level value less than 13
                drain_water(45) # drain water for 10 seconds
                 # stage 1 completed

                # Example usage
                update_progress("17348502838715973", 1000, "39")
                write_data_to_shared_memory("command_from_server", 39.0)

            except Exception as e:
                dummy =1
            



        elif command <=39.0:
            try:                    
                # stage 2
                # load_water(120) # load water for 10 seconds

                check_and_load_water(13) # load water while reaching the level value less than 13

                # Example usage
                update_progress("17348502838715973", 1000, "68")
                write_data_to_shared_memory("command_from_server", 68.0)

            except Exception as e:
                dummy =1
            



        elif command <=68.0:
            try:                    
                send_rpm(8000)
                drum_rotation_pattern_two()

                # Example usage
                update_progress("17348502838715973", 1000, "80")
                write_data_to_shared_memory("command_from_server", 80.0)

            except Exception as e:
                dummy =1
            



        elif command <=80.0:
            try:                    
                
                check_and_load_water(13) # load water while reaching the level value less than 13

                # Example usage
                update_progress("17348502838715973", 1000, "90")
                write_data_to_shared_memory("command_from_server", 90.0)

            except Exception as e:
                dummy =1
            




        elif command <=90.0:
            try:                    

                drain_water(45) # drain water for 10 seconds

                # Example usage
                update_progress("17348502838715973", 1000, "99")
                write_data_to_shared_memory("command_from_server", 99.0)
 
            except Exception as e:
                dummy =1
            


#hello
            i=1
        elif command <=99.0:
            try:                    
                open_door()

                # Example usage
                update_ready("17348502838715973", 1000)

                write_data_to_shared_memory("command_from_server", 1000.0)
                cycle_end()
            except Exception as e:
                dummy =1
            

        else:
            time.sleep(4)  # Adjust the delay as needed



def exit_handler():
    """Set all relay pins to HIGH state on exit."""
    dummy =1
    write_data_to_shared_memory("relay_command", 14.0)




if __name__ == "__main__":
    # Start the shared memory reader thread
    reader_thread = threading.Thread(target=read_shared_memory, daemon=True)
    reader_thread.start()

    # Start the door control procedure thread
    control_thread = threading.Thread(target=door_control_procedure, daemon=True)
    control_thread.start()

    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated.")
    finally:
        exit_handler()

