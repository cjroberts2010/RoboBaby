"""!
@file main.py

@brief This file will run a series of tasks during operation and idle states.
@detail This file contains a scheduler and initializes all hardware and software
        in order to properly operate the system.
   @author Christian Roberts
   @author Matteo Gozzini
   @author Grace Mekrut
   @author Miles Ibarra
   @author JR Ridgely

@date   2022-04-04 Updated template from basictasks.py, created by JR Ridgely.
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2.
"""


# Revision History-----------------------------------------------------------
# 
# Revision A: Created code architecture and defined functions to complete
# 04-04-22
# 

import gc
import pyb
import cotask
import task_share
import math
import PIR
import OilSound
import utime
import mos

from pyb import USB_VCP
vcp = USB_VCP()

def task1_PIR ():

    """!
    Generator task which controls the PIR reader.
    """
    counter = 0
    while True:
        val = PinPIR.read()
        if val == 1:
            S_PIR_flag.put(1)
        else:
            S_PIR_flag.put(0)
        counter += 1
        yield (0)

def task2_MP () :
    
    """!
    Generator task which controls the Microphone reader
    """
    counter = 0
    state = '0_init'
    while True:
        flag = S_MP_flag.get()
        print(state)
        if flag == 0:
            if state == '0_init':
                last_time = utime.ticks_ms()
                check_time = utime.ticks_ms()
                delta = utime.ticks_diff(last_time, check_time)
                state = '1_listen'
                yield()
                
            elif state == '1_listen':
                val = PinMP.read()
                if val > 500:
                    state = '2_wait'
                    last_time = utime.ticks_ms()
                    yield()
                else:
                    yield()
                    
            elif state == '2_wait':
                val = PinMP.read()
                check_time = utime.ticks_ms()
                delta = utime.ticks_diff(check_time, last_time)
                if val>500 and delta > 5000:
                    S_MP_flag.put(1)
                    state = '1_listen'
                    yield()
                else:
                    yield()

def task3_states () :
    last_time = utime.ticks_ms()
    state = 0
    while True:
        pir = S_PIR_flag.get()
        mp = S_MP_flag.get()
        this_time = utime.ticks_ms()
        diff = utime.ticks_diff(this_time, last_time)
        if state == 0:
            if diff >= 1000 and pir == 1 and mp == 1:
                state+=1
                yield()
            else:
                yield()
        elif state == 1:
            S_MOSFET_flag.put(1)
            state = 0
            yield()
            
def task4_mosfets() :
    while True:
        val = S_MOSFET_flag.get()
        if val == 1:
            mos.pulse()
            yield()
        else:
            yield()
            
            
            
            
            
            
def test_shares():
    print('PIR = ' + str(S_PIR_flag.get()))
    print('MP = ' + str(S_MP_flag.get()))
    print('Timer = ' + str(S_Timer_flag.get()))
    print('MOSFET = ' + str(S_MOSFET_flag.get()))
    
    
        
# This code creates a 8 shares and 8 tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    try:
        
        #Create Shares to hold flags.
        # Create a share to hold the PIR flag.
        S_PIR_flag = task_share.Share ('l', thread_protect = False, name = "S_PIR_flag")
        
        #Create a share to hold the microphone flag.
        S_MP_flag = task_share.Share ('l', thread_protect =False, name = "S_MP_flag")
        
        #Create a share to hold the timer flag.
        S_Timer_flag = task_share.Share ('l', thread_protect = False, name = "S_Timer_flag")
        
        #Create a share to hold the MOSFET flag.
        S_MOSFET_flag = task_share.Share ('l', thread_protect = False, name = "S_MOSFET_flag")
        
        #Fill all flags with zeros in intial states.
        S_PIR_flag.put(0)
        S_MP_flag.put(0)
        S_Timer_flag.put(0)
        S_MOSFET_flag.put(0)
        
        #Create objects to use in the tasks.
        PinPIR = PIR.PIR(pyb.Pin.board.PA9)
        PinMP = pyb.ADC(pyb.Pin.board.PA0)
            
        # Create the tasks. In order to create a task, refer to a task function, and give the task
        # a priority and period to run. Safety critical components should run faster, and encoders
        # should run faster than motors. 
        task1 = cotask.Task (task1_PIR, name = 'Task_1', priority = 1, 
                             period = 30, profile = True, trace = False)
        
        task2 = cotask.Task (task2_MP, name = 'Task_2', priority = 1,
                             period = 30, profile = True, trace = False)
        
        task3 = cotask.Task (task3_states, name = 'Task_3', priority = 1,
                             period = 30, profile = True, trace = False)
        
        task4 = cotask.Task (task4_mosfets, name = 'Task_4', priority = 1,
                             period = 30, profile = True, trace = False)
        
        cotask.task_list.append (task1)
        cotask.task_list.append (task2)
        cotask.task_list.append (task3)
        cotask.task_list.append (task4)

        # Run the memory garbage collector to ensure memory is as defragmented as
        # possible before the real-time scheduler is started
        gc.collect ()

        # Run the scheduler with the chosen scheduling algorithm. Quit if any 
        # character is received through the serial port
        vcp = pyb.USB_VCP ()
        while not vcp.any ():
            cotask.task_list.pri_sched ()

        # Empty the comm port buffer of the character(s) just pressed
        vcp.read ()
    except KeyboardInterrupt:
        # Print a table of task data and a table of shared information data
        print ('\n' + str (cotask.task_list))
        print (task_share.show_all ())
        print (task1.get_trace ())
        print ('\r\n')
        test_shares()
