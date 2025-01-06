import requests
import time
from shared_memory_util import write_data_to_shared_memory
from datetime import datetime

# API URL
url = "http://srv630050.hstgr.cloud:3000/api/device/checkjobs"

# JSON data to send in the request
data = {
    "hubid": "17348502838715973",
    "deviceid": 1000
}

try:
    print("Starting job check loop... Press Ctrl+C to stop.")
    while True:
        try:
            # Make a POST request to the API with a timeout
            response = requests.post(url, json=data, timeout=10)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                response_data = response.json()
                
                # Extract devicestatus and convert it directly to a float
                devicestatus = float(response_data.get('devicestatus', 0))
                
                # print(f"[{datetime.now()}] Numeric devicestatus received: {devicestatus}")

                # Write the float value to shared memory
                write_data_to_shared_memory("command_from_server", devicestatus)
            
            elif response.status_code == 204:
                # No job available, set command to 0.0
                # print(f"[{datetime.now()}] No job available")
                write_data_to_shared_memory("command_from_server", 1000.0)
            else:
                # print(f"[{datetime.now()}] Failed to call API. Status Code: {response.status_code}")
                # print(f"Response: {response.text}")
                dummy =1
        
        except requests.exceptions.RequestException as e:
            # print(f"[{datetime.now()}] API request error: {e}")
            dummy =1
        
        # Wait for 5 seconds before the next request
        time.sleep(5)

except KeyboardInterrupt:
    print("\nJob checking loop stopped by user.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
