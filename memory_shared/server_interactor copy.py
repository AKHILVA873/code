import requests
import json
import time
from shared_memory_util import read_data_from_shared_memory, write_data_to_shared_memory
# API URL
url = "http://srv630050.hstgr.cloud:3000/api/device/checkjobs"

# JSON data to send in the request
data = {
    "hubid" : "17348502838715973",
    "deviceid": 1000
}

try:
    print("Starting job check loop... Press Ctrl+C to stop.")
    while True:
        # Make a POST request to the API
        response = requests.post(url, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Print the JSON response
            print("Response:")
                        # Extract the JSON response
            response_json = response.json()
            # Extract devicestatus and check if it's "Booked"
            devicestatus = response_json.get("devicestatus", "")
            
            if devicestatus == "0":
                print("Booked")
                write_data_to_shared_memory("command_from_server", 1.0)
            else:
                print("Not Booked")
                write_data_to_shared_memory("command_from_server", 0.0)


            # print(json.dumps(response.json(), indent=4))
        else:
            print(f"Failed to call API. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Wait for 3 seconds before the next request
        time.sleep(5)

except KeyboardInterrupt:
    print("\nJob checking loop stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")

