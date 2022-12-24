### About this code
This Python script checks for internet connectivity and launches Discord and LINE if they are not already running.

The script begins by importing several libraries, including:
* `socket`
* `subprocess`
* `time`
* `psutil`
* `logging`
* `msvcrt`
* `os`
* `requests`

The `logging` library is used to log messages to the console at different levels (e.g., `INFO`, `WARNING`). The `msvcrt` library is used to pause the program and wait for user input.

### Warnings

There are a few potential warnings to consider when using this code:

1. The script relies on the environment variables `DISCORD_PATH` and `LINE_PATH` being set to the correct paths of Discord and LINE, respectively. If these variables are not set or are set to the wrong paths, the script will not be able to launch the programs.
2. The script enters an infinite loop and continually prompts the user to press any key to reconnect if internet connectivity is not detected. This can be frustrating for the user if they are unable to connect to the internet. It may be advisable to add a limit to the number of times the user is prompted to reconnect before the script exits.
