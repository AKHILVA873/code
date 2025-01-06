import redis
import struct

# Connect to Redis (make sure Redis server is running)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)

def create_shared_memory(name, size):
    # Redis handles dynamic storage, so no explicit size is needed
    if not r.exists(name):  # Check if the key exists
        r.set(name, struct.pack('f', 0.0))  # Initialize with a default value
    return r

def write_data_to_shared_memory(name, data):
    # Write data to Redis, pack as a float using struct
    byte_data = struct.pack('f', data)
    r.set(name, byte_data)

def read_data_from_shared_memory(name):
    # Read the byte data from Redis and unpack it
    byte_data = r.get(name)
    if byte_data:
        data = struct.unpack('f', byte_data)[0]
        return data
    else:
        return None  # Return None if the key does not exist

def modify_shared_memory(name, modify_func):
    # Read current value, apply modify_func, and save the updated value
    current_data = read_data_from_shared_memory(name)
    if current_data is not None:
        modified_data = modify_func(current_data)
        write_data_to_shared_memory(name, modified_data)
