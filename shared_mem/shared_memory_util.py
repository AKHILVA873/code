from multiprocessing import shared_memory
import struct

def create_shared_memory(name, size):
    try:
        shm = shared_memory.SharedMemory(name=name, create=True, size=size)
        return shm
    except FileExistsError:
        shm = shared_memory.SharedMemory(name=name)
        return shm

def write_data_to_shared_memory(name, data):
    shm = shared_memory.SharedMemory(name=name)
    byte_data = struct.pack('f', data)
    shm.buf[:4] = byte_data
    shm.close()

def read_data_from_shared_memory(name):
    shm = shared_memory.SharedMemory(name=name)
    byte_data = bytes(shm.buf[:4])
    data = struct.unpack('f', byte_data)[0]
    shm.close()
    return data

def modify_shared_memory(name, modify_func):
    shm = shared_memory.SharedMemory(name=name)
    byte_data = bytes(shm.buf[:4])
    data = struct.unpack('f', byte_data)[0]
    modified_data = modify_func(data)
    shm.buf[:4] = struct.pack('f', modified_data)
    shm.close()
