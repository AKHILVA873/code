"""
*******************************************************************************
*                                                                             *
*  Copyright (c) [dd-mm-yyyy] Hutlabs                                         *
*  All rights reserved.                                                       *
*                                                                             *
*  Developed by: AKHIL VA                                                     *
*                Software Engineer                                             *
*                                                                             *
*  Contact: akhilva@am.amrita.edu                                              *
*           akhilva.in@gmail.com                                               *
*                                                                             *
*  This software may be modified and distributed under the terms              *
*  of the MIT license. See the LICENSE file for details.                      *
*                                                                             *
*******************************************************************************
"""





from multiprocessing import shared_memory
import time



def write_data_to_shared_memory(shared_memory_name, data):
    try:
        shm = shared_memory.SharedMemory(create=True, size=1, name=shared_memory_name)
        shm.buf[0] = data
        return shm
    except FileExistsError:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        print("Shared memory segment already exists.")
        return shm
    except Exception as e:
        print("Error:", e)
        return None
    



def read_data_from_shared_memory(shared_memory_name):
    try:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        data = shm.buf[0]
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
    try:
        shm = shared_memory.SharedMemory(name=shared_memory_name)
        shm.buf[0] = new_data
        # print(f"Data in shared memory '{shared_memory_name}' modified to '{new_data}'.")
    except FileNotFoundError:
        print(f"Shared memory '{shared_memory_name}' not found.")
    except Exception as e:
        print("Error:", e)
    finally:
        if shm:
            shm.close()