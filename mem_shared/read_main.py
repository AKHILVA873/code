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
from shared_memory_util import read_data_from_shared_memory
import time

if __name__ == "__main__":
    shared_memory_name = "demo_shared_memory_single_float"

    while True:
        data = read_data_from_shared_memory(shared_memory_name)
        if data is not None:
            print("data is:",data)
            # if data > 4:
            #     print("Data is greater than 4.")
            # else:
            #     print("Data is less than or equal to 4.")
        else:
            print("No data read from shared memory.")

        time.sleep(1)
