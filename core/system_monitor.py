import psutil
import time


def get_system_status():

    cpu = psutil.cpu_percent()

    memory = psutil.virtual_memory().percent

    uptime = time.time()

    return {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "system_uptime": uptime
    }