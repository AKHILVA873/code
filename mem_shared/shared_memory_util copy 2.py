from multiprocessing import shared_memory
import struct

def write_data_to_shared_memory(shared_memory_name, data, size=4):
    try:
        shm = shared_memory.SharedMemory(create=True, size=size, name=shared_memory_name)
        struct.pack_into('f', shm.buf, 0, data)  # Use 'f' for float
        return shm
    except FileExistsError:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        struct.pack_into('f', shm.buf, 0, data)  # Use 'f' for float
        print("Shared memory segment already exists.")
        return shm
    except Exception as e:
        print("Error:", e)
        return None

def read_data_from_shared_memory(shared_memory_name):
    shm = None
    try:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        data = struct.unpack_from('f', shm.buf, 0)[0]  # Use 'f' for float
        return data
    except FileNotFoundError:
        print(f"Shared memory '{shared_memory_name}' not found.")
        return None
    except Exception as e:
        print("Error:", e)
        return None
    finally:
        if shm:
            shm.close()

def modify_shared_memory_data(shared_memory_name, new_data):
    shm = None
    try:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        struct.pack_into('f', shm.buf, 0, new_data)  # Use 'f' for float
        print(f"Data in shared memory '{shared_memory_name}' modified to '{new_data}'.")
    except FileNotFoundError:
        print(f"Shared memory '{shared_memory_name}' not found.")
    except Exception as e:
        print("Error:", e)
    finally:
        if shm:
            shm.close()
