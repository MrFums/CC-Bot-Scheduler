import ctypes
import threading
import time
import socket
import os
import configparser
import sys
import psutil
import pydirectinput
import schedule
import discord
import logging

# Function to check if the script is running with administrator privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to restart the script with administrator privileges
def restart_as_admin():
    try:
        if sys.version_info[0] == 3 and sys.version_info[1] >= 5:
            script = os.path.abspath(__file__)
            params = ' '.join([script] + sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        else:
            raise RuntimeError("This script requires Python 3.5 or higher.")
    except Exception as e:
        logging.error(f"Failed to elevate privileges: {e}")
        sys.exit(1)

# Request to run the script with administrator privileges if not already running as admin
if not is_admin():
    logging.warning("Requesting admin privileges...")
    restart_as_admin()
    sys.exit()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

helpContent = '''
```++help - this command
++togglef1 - toggles F1 time scheduling based on the local time you set in config.ini
++uptime - reports the uptime of the HOST MACHINE and also the hostname the bot is running on
++start - starts the bot (presses f1)
++pr - pause / resume the bot (presses f5)
++terminate - terminates the bot (presses f3)```
'''

# Configuration setup
config_file = 'config.ini'
config = configparser.ConfigParser()

# Check if config file exists, if not, create it with default values
if not os.path.exists(config_file):
    logging.info("Config file not found. Creating config file with default values.")
    config['DEFAULT'] = {
        'Token': 'your_token_here',
        'LocalResetTime': '11:00'
    }
    with open(config_file, 'w') as f:
        config.write(f)

# Read the config file
config.read(config_file)
token = config['DEFAULT']['Token']
localResetTime = config['DEFAULT']['LocalResetTime']

def killGFN():
    logging.info("Attempting to kill GeForce Now processes.")
    for process in psutil.process_iter(['pid', 'name']):
        if 'GeForceNOW.exe' in process.info['name']:
            logging.info(f"Killing GeForce Now process with PID {process.info['pid']}")
            process.kill()
        elif 'GeForceNOWContainer.exe' in process.info['name']:
            logging.info(f"Killing GeForce Now Container process with PID {process.info['pid']}")
            process.kill()
    time.sleep(10)
    return

# Function to send F1 key command
def send_f1_command():
    logging.info("Sending F1 command.")
    killGFN()
    time.sleep(3)
    pydirectinput.press('f3')
    time.sleep(3)
    pydirectinput.press('f1')

# Toggle flag to control the scheduler
is_scheduled = False
schedule_lock = threading.Lock()

def getUptime():
    # getting the library in which GetTickCount64() resides
    lib = ctypes.windll.kernel32

    # calling the function and storing the return value
    t = lib.GetTickCount64()

    # since the time is in milliseconds i.e. 1000 * seconds
    # therefore truncating the value
    t = int(str(t)[:-3])

    # extracting hours, minutes, seconds & days from t
    # variable (which stores total time in seconds)
    mins, sec = divmod(t, 60)
    hour, mins = divmod(mins, 60)
    days, hour = divmod(hour, 24)

    # formatting the time in readable form
    # (format = x days, HH:MM:SS)
    currentUptime = f'{days}d {hour}h {mins}m {sec}s on {socket.gethostname()}'
    return currentUptime

# Function to toggle scheduling
def schedule_f1():
    global is_scheduled
    with schedule_lock:
        if not is_scheduled:
            schedule.every().day.at(localResetTime).do(send_f1_command)
            is_scheduled = True
            logging.info(f"F1 scheduling started. Reset time is local {localResetTime}")
        else:
            schedule.clear()
            is_scheduled = False
            logging.info("F1 scheduling stopped.")

# Function to run the scheduler
def run_scheduler():
    while True:
        with schedule_lock:
            schedule.run_pending()
        time.sleep(1)

# Start the scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# Discord event - bot ready
@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="++ Scheduling: Disabled"))

# Discord event - message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('++togglef1'):
        schedule_f1()
        status = "started" if is_scheduled else "stopped"
        await message.channel.send(f'F1 scheduling has been {status} for reset time {localResetTime}')
        logging.info(f'F1 scheduling has been {status} for reset time {localResetTime}')

        if is_scheduled:
            await client.change_presence(activity=discord.Game(name="++ Scheduling: Enabled"))
        else:
            await client.change_presence(activity=discord.Game(name="++ Scheduling: Disabled"))

    if message.content.startswith('++uptime'):
        uptime = getUptime()
        await message.channel.send(f'Uptime is {uptime}')
        logging.info(f'Uptime is {uptime}')

    if message.content.startswith('++start'):
        pydirectinput.press('f1')
        await message.channel.send(f'Starting bot')
        logging.info('Starting bot')

    if message.content.startswith('++pr'):
        pydirectinput.press('f5')
        await message.channel.send(f'Pausing or resuming bot')
        logging.info('Pausing or resuming bot')

    if message.content.startswith('++terminate'):
        pydirectinput.press('f3')
        await message.channel.send(f'Terminate bot')
        logging.info('Terminate bot')
        
    if message.content.startswith('++help'):
        await message.channel.send(helpContent)
        logging.info('Help')

# Run the Discord client with error handling
try:
    client.run(token)
except discord.errors.LoginFailure:
    logging.error("Failed to log in to Discord. Check your token in the config file.")
    while True:
        time.sleep(1)  # Keep the program running to allow log inspection
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    while True:
        time.sleep(1)  # Keep the program running to allow log inspection
