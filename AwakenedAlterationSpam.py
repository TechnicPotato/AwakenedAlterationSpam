import keyboard
import pyautogui
import pyperclip
import time
import re
import sys
import random

SAFETY_LIMIT = 40  # Max number of roll attempts before exiting

running = False
user_regex = ""

# Need this to output the number of lines obtained from an alteration orb in order to determine if an aug needs to be used.
def extract_item_name(text):
    lines = text.splitlines()
    capture = False
    extracted = []
    # Check number of lines scanned here and output as a seperate line
    linecount = count(lines)
    for line in lines:
        if line.startswith("Rarity:"):
            capture = True
            continue
        if line.strip() == "--------" and capture:
            break
        if capture:
            extracted.append(line)

    return "\n".join(extracted), linecount

def start():
    global running, user_regex
    if not running:
        running = True
        print("Program started.")

        attempts = 0
        attempt_width = len(str(SAFETY_LIMIT))  # Align width based on safety_limit
        # Py Auto GUI can be used here to hold the shift key
        # Keydown.
        while attempts < SAFETY_LIMIT:
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)
            raw_text = pyperclip.paste()

            # Extract and clean item name
            item_name = extract_item_name(raw_text)
            item_name = "".join(line.lstrip() for line in item_name.splitlines())

            # Check for regex match
            if re.search(user_regex, item_name):
                print("Match found. Exiting.")
                keyboard.unhook_all_hotkeys()
                sys.exit(0)

            # Check if Augmentation can be used
            
            # Print formatted attempt log
            print(f"Attempt {str(attempts + 1).rjust(attempt_width)}: Regex: {user_regex} Item Name: {item_name}")
            pyautogui.click()
            attempts += 1
            # Add random interval sanity for macro checks
            time.sleep(random.uniform(0.07, 0.12))

        print(f"Reached safety limit of {safety_limit} attempts. Exiting.")
        running = False

def stop():
    global running
    if running:
        running = False
        print("Program stopped.")

# Ask user for safety limit (default to 40 if invalid)
try:
    user_input = input("Enter safety limit [40] (max attempts before auto-stop): ").strip()
    SAFETY_LIMIT = int(user_input) if user_input else 40
except ValueError:
    SAFETY_LIMIT = 40
print(f"Using safety limit: {SAFETY_LIMIT}")

# Ask user for regex
user_regex = input("Enter regex to match item name: ")

keyboard.add_hotkey('shift+=', start)
keyboard.add_hotkey('shift+-', stop)

print("Waiting for Shift+= to start, Shift+- to stop.")
print("Press Ctrl+C to exit manually if needed.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting on Ctrl+C")
