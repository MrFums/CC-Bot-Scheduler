# Discord Bot for CC

This is a Python-based Discord bot that automates certain actions for CC. The bot uses a scheduler to perform these actions at a specific time each day.

## Features

- **Scheduler**: Automates actions at a specified time each day.
- **Discord Commands**: Allows control of the bot via Discord messages.

## Prerequisites

- Python 3.6 or higher
- Administrator privileges to run the script
- CC

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MrFums/CC-Bot-Scheduler.git
    cd CC-Bot-Scheduler
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configuration**:
   - Creates a `config.ini` file in the project directory if it doesn't already exist.
   - The script will create this file with default values if it doesn't find it.
   - Modify `config.ini` to add your Discord bot token and desired reset time:
     ```ini
     [DEFAULT]
     Token = your_token_here
     LocalResetTime = 11:00
     ```

## Usage

1. **Run the script**:
    ```bash
    python BotScheduleCC.py
    ```
    OR

  **Run the complied executable**:
   - Head over to the releases tab and download the .exe and run it. You don't need to install python or any dependency for this.
   

3. **Discord Commands**:
   - `++gelp`: Show all commands and a description.
   - `++togglef1`: Start/stop the scheduled F1 command.
   - `++uptime`: Get the system uptime.
   - `++start`: Manually send the F1 command.
   - `++pr`: Pause or resume the bot.
   - `++terminate`: Terminate the bot.

4. **Disclaimer**:
   - You require to manually open CC and leave it setup. I would highly advise you set it up to return to character at cycler position 0 once it is complete to allow this script to seamlessly work.
   - This script is not anywhere near as intuitive as CC, it quite literally JUST presses F1 at the time you set, nothing else fancy.

## Script Explanation

### Main Components

- **Privilege Elevation Check and Restart**:
  Ensures the script runs with administrator privileges.
  
- **Configuration File Setup**:
  Creates and reads from a `config.ini` file, including default values for `Token` and `LocalResetTime`.

- **Discord Bot Setup**:
  Initializes the Discord bot with the specified intents and sets up event handlers.

- **Scheduler**:
  Automates actions at a specified time each day.

### Why?

- You can run this on a second throwaway PC or thinclient and have a reset time set, the bot will then automatically run CC at the set time without you having to even think about it.

### Functions

- `is_admin()`: Checks if the script is running with administrator privileges.
- `restart_as_admin()`: Restarts the script with administrator privileges if not already running as admin.
- `killGFN()`: Kills GeForce Now processes.
- `send_f1_command()`: Sends F1 key command and kills GeForce Now processes.
- `getUptime()`: Returns the system uptime.
- `schedule_f1()`: Toggles the scheduling of the F1 command.
- `run_scheduler()`: Runs the scheduler.

## Contributing

If you have any suggestions or improvements, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License.
