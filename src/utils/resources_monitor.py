"""File description:

Auxiliary file for measuring the execution time and CPU utilization.
"""

import os
import threading
import time

import psutil

# resource usage measurement section
thread_running = cpu_thread = start_time = avg_cpu_percentage = None

# measure interval
measure_interval = 0.01  # the minimum is 0.01

# Function to continuously measure CPU percentage
def measure_cpu():
    global avg_cpu_percentage, measure_interval

    # Multi-platforms
    cpu_load_sum = 0
    cpu_load_quantity = 0

    while thread_running:
        cpu_percentage = psutil.cpu_percent(interval=measure_interval, percpu=False)
        cpu_load_sum += cpu_percentage
        cpu_load_quantity += 1
        time.sleep(measure_interval)

    avg_cpu_percentage = cpu_load_sum / cpu_load_quantity


def monitor_tic():
    global thread_running, cpu_thread, start_time

    thread_running = True
    cpu_thread = threading.Thread(target=measure_cpu)
    cpu_thread.start()
    start_time = time.perf_counter()

def monitor_toc():
    global thread_running, cpu_thread, start_time, avg_cpu_percentage

    # Stop measuring time
    end_time = time.perf_counter()

    # Stop the CPU measurement thread
    thread_running = False
    cpu_thread.join()

    # In case this function is called in less than measure_interval seconds since the tic function
    while avg_cpu_percentage == 0:
        time.sleep(measure_interval)
        avg_cpu_percentage = psutil.cpu_percent(interval=measure_interval, percpu=False)

    # Calculate the elapsed time
    return end_time - start_time, avg_cpu_percentage
