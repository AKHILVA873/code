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
from shared_memory_util import write_data_to_shared_memory
import time
import atexit

def cleanup_shared_memory(shm):
    def cleanup():
        print("Cleaning up shared memory.")
        shm.close()
        shm.unlink()
    return cleanup

if __name__ == "__main__":
    # Write float data to shared memory
    shm = write_data_to_shared_memory("demo_shared_memory_single_float", 2000.789, size=4)
    if shm:
        atexit.register(cleanup_shared_memory(shm))
        print(f"Float data written to shared memory.")
    
    while True:
        time.sleep(1)  # Keeping the process alive to maintain the shared memory
