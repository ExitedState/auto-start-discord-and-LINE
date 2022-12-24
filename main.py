import socket
import subprocess
import time
import psutil
import logging
import msvcrt
import os
import requests

logging.basicConfig(level=logging.INFO)


def check_internet_connectivity(timeout=2):
    # Send a simple HTTP request to a web server
    try:
        response = requests.head("http://www.google.com", timeout=timeout)
        logging.info(f"HTTP response code: {response.status_code}")
        if 200 <= response.status_code < 400:
            logging.info("Internet connectivity detected via HTTP request.")
            return True
    except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
        pass

    # Check if we can ping a known stable server
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
            ("1.1.1.1", 53))
        logging.info(
            "fantastic Internet connectivity detected via ping. this is mean google lost server")
        return True
    except socket.error:
        pass

    logging.warning(
        "No internet connectivity detected. Please connect to the internet and try again.")
    return False


def check_if_process_running(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except psutil.NoSuchProcess:
            pass
    return False


def launch_program(program_name, program_path):
    if not check_if_process_running(program_name):
        try:
            subprocess.run(program_path, start_new_session=True)
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
    while True:
        all_launched = True
        if check_internet_connectivity():
            time.sleep(3)
            for program_name, program_path in programs.items():
                if program_name in approved_programs:
                    if not launch_program(program_name, program_path):
                        all_launched = False
                        break
                else:
                    logging.warning(
                        f"{program_name} is not an approved program and will not be launched.")
        if all_launched and check_if_process_running("discord") and check_if_process_running('line'):
            break
        logging.warning("Press any key to reconnect...")
        msvcrt.getch()
        os.system('cls')


if __name__ == '__main__':
    main(approved_programs)
