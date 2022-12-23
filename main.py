import socket
import subprocess
import time
import psutil
import logging
import msvcrt
import os

logging.basicConfig(level=logging.INFO)

def check_internet_connectivity(host="1.1.1.1", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        logging.warning("No internet connectivity detected. Please connect to the internet and try again.")
        return False

def check_if_process_running(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

os.environ['DISCORD_PATH'] = 'C:\\Users\\phaib\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe'
os.environ['LINE_PATH'] = 'C:\\Users\\phaib\\AppData\\Local\\LINE\\bin\\LineLauncher.exe'

approved_programs = {
    'discord': os.environ['DISCORD_PATH'],
    'line': os.environ['LINE_PATH']
}

import subprocess

def main(programs):
    while True:
        if check_internet_connectivity():
            logging.info("Welcome! Starting programs in 3 seconds...")
            # Use subprocess.run() to run the 'sleep 3' command, which will pause the program for 3 seconds
            subprocess.run('sleep 3')
            for program_name, program_path in programs.items():
                if program_name in approved_programs:
                    if not check_if_process_running(program_name):
                        try:
                            subprocess.Popen(program_path, start_new_session=True)
                            logging.info(f"Opening {program_name.capitalize()}")
                            # Use subprocess.run() to run the 'sleep 5' command, which will pause the program for 5 seconds
                            subprocess.run('sleep 5')
                        except FileNotFoundError:
                            flag = True
                            break
                else:
                    logging.warning(f"{program_name} is not an approved program and will not be launched.")
        if check_if_process_running("discord") and check_if_process_running('line'):
            logging.info("All programs are running.\nPress any key to exit...")
            msvcrt.getch()
            break
        if flag:
            logging.warning("One or more programs could not be found. Please check your program paths and try again.\nPress any key to exit...")
            msvcrt.getch()
            break
        logging.warning("Reconnecting in 5 seconds...\nPress any key to reconnect...")
        msvcrt.getch()
        os.system('cls')


if __name__ == '__main__':
    main(approved_programs)