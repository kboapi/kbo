import uiautomator2 as u2
import subprocess
import time

# Connect to the device
d = u2.connect()

# Ensure the screen is on
d.screen_on()

# Use `adb shell` to perform additional tasks
def run_adb_command(cmd):
    """Run an ADB shell command and print the output."""
    result = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)

# Example ADB commands
run_adb_command("input keyevent KEYCODE_WAKEUP")  # Turn on the screen
run_adb_command("input swipe 300 1000 300 500")  # Swipe up (for swipe unlock)
