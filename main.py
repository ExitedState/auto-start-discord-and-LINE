import logging
import os
import psutil
import requests
import socket
import subprocess
import time

logging.basicConfig(level=logging.INFO)

def check_internet_connectivity(timeout=0.5):
    """
    Check if the device is connected to the internet.
    
    This function checks for internet connectivity by attempting to
    ping a known stable server and send a simple HTTP request to a web server.
    
    Parameters:
    timeout (float): The number of seconds to wait for a response before giving up.
    
    Returns:
    bool: True if internet connectivity was detected, False otherwise.
    """
    # Check if we can ping a known stable server
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("1.0.0.1", 53))
        logging.info("Internet connectivity detected via DNS query to Cloudflare's DNS server.")
        return True
    except socket.error:
        pass
    # Send a simple HTTP request to a web server
    try:
        response = requests.head("http://www.google.com", timeout=timeout)
        logging.info(f"HTTP response code: {response.status_code}")
        if 200 <= response.status_code < 400:
            logging.info("Internet connectivity detected via HTTP request.")
            return True
    except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
        pass

    logging.warning(
        "No internet connectivity detected. Please connect to the internet and try again.")
    return False

def check_if_process_running(process_name):
    """
    Check if a process with the given name is running.
    
    This function searches for a process with the given name using the
    psutil library.
    
    Parameters:
    process_name (str): The name of the process to search for.
    
    Returns:
    bool: True if the process was found, False otherwise.
    """
    for pid in psutil.pids():
        try:
            proc = psutil.Process(pid)
            if process_name.lower() in proc.name().lower():
                return True
        except psutil.NoSuchProcess:
            pass
    return False

def launch_program(program_name, program_path):
    """
    Launch a program if it is not already running.
    
    This function uses the subprocess library to launch the given program.
    
    Parameters:
    program_name (str): The name of the program to launch.
    program_path (str): The file path of the program to launch.
    
    Returns:
    bool: True if the program was launched or was already running, False if an error occurred.
    """
    if not check_if_process_running(program_name):
        try:
            subprocess.Popen(program_path, start_new_session=True)
            logging.info(f"Opening {program_name.capitalize()}")
            time.sleep(5)
        except FileNotFoundError:
            logging.warning(
                f"{program_name} could not be found. Please check your program path and try again.")
            return False
    return True


os.environ['DISCORD_PATH'] = 'C:\\Users\\phaib\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe'
os.environ['LINE_PATH'] = 'C:\\Users\\phaib\\AppData\\Local\\LINE\\bin\\LineLauncher.exe'

approved_programs = {
    'discord': os.environ['DISCORD_PATH'],
    'line': os.environ['LINE_PATH']
}

def main(programs):
    """
    Main function to launch approved programs.
    
    This function continually checks for internet connectivity and launches
    approved programs if they are not already running. The function exits
    when all approved programs have been successfully launched.
    
    Parameters:
    programs (dict): A dictionary of approved programs, where the keys are the
        names of the programs and the values are the file paths.
    """
    while True:
        all_launched = True
        if check_internet_connectivity():
            time.sleep(3)
            for program_name, program_path in programs.items():
                if not launch_program(program_name, program_path):
                    all_launched = False
                    break
        if all_launched:
            break
        logging.warning("Press any key to reconnect...")
        input()
        os.system('cls')

if __name__ == '__main__':
    main(approved_programs)
