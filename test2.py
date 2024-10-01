from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import os
import random
import traceback
import time
import uuid
import subprocess
import platform
import requests
from config import api_id, api_hash, phone, session_name, target

# Function to get and store device ID for Windows
def get_windows_device_id():
    device_id_file = "windows_device_id.txt"  # File to store the device ID for Windows

    # Check if device ID already exists
    if os.path.exists(device_id_file):
        with open(device_id_file, "r") as f:
            return f.read().strip()
    
    # Generate a device ID based on the Volume Serial Number for Windows
    device_id = get_windows_volume_serial()

    if device_id:
        # Store the device ID in a file for future use
        with open(device_id_file, "w") as f:
            f.write(device_id)
    
    return device_id

# Function to get and store device ID for Android/Linux
def get_android_device_id():
    device_id_file = "android_device_id.txt"  # File to store the device ID for Android/Linux

    # Check if device ID already exists
    if os.path.exists(device_id_file):
        with open(device_id_file, "r") as f:
            return f.read().strip()

    # Generate a device ID based on the MAC address for Android/Linux
    device_id = hex(uuid.getnode())  # This uses the device's MAC address as the unique identifier

    if device_id:
        # Store the device ID in a file for future use
        with open(device_id_file, "w") as f:
            f.write(device_id)
    
    return device_id

# Function to get the Volume Serial Number on Windows
def get_windows_volume_serial():
    try:
        # Use subprocess to run the 'wmic' command and get the serial number
        result = subprocess.run(["wmic", "volume", "get", "serialnumber"], capture_output=True, text=True)

        print(f"WMIC Output: {result.stdout}")  # Debugging: Print the raw output from WMIC

        if result.returncode != 0:
            raise Exception(f"wmic command failed with return code {result.returncode}")

        # Split the output and filter out empty lines
        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

        # Ensure that we have at least two lines (header and serial number)
        if len(lines) < 2:
            raise Exception("No serial number found in WMIC output")

        serial_number = lines[1]  # The serial number should be on the second line
        return serial_number
    except Exception as e:
        print(f"Error fetching volume serial number: {e}")
        return None

# Function to verify the license
def check_license(license_key, device_id):
    if device_id is None:
        print("Unable to retrieve device ID")
        sys.exit()

    # Print device ID for debugging
    print(f"Device ID: {device_id}")

    # Send request to PHP API for license verification
    response = requests.post("https://blaze.freecodes.in/verify_license.php", data={
        'license_key': license_key,
        'device_id': device_id
    })

    # Debugging: Print server response
    print(f"Response from server: {response.text}")

    try:
        return response.json()
    except ValueError:
        print("Failed to decode JSON from server response.")
        sys.exit()

# Function to add user to a group for Windows
def add_user_windows():
    license_key = input("Enter your license key: ")
    device_id = get_windows_device_id()
    result = check_license(license_key, device_id)

    if result['status'] != 'success':
        print(f"License verification failed: {result['message']}")
        sys.exit()

    print("License verified! Proceeding with adding user on Windows...")

    print('Initializing Telegram client...')
    client = TelegramClient(str(session_name), api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    # Add user functionality here
    user_to_add = input("Enter the username or ID of the user to add: ")

    try:
        user = client.get_input_entity(user_to_add)
        client(functions.channels.InviteToChannelRequest(
            channel=target,
            users=[user]
        ))
        print(f"User {user_to_add} added successfully to the group on Windows!")
    except Exception as e:
        print(f"Failed to add user {user_to_add}: {e}")

# Function to add user to a group for Android/Linux
def add_user_android():
    license_key = input("Enter your license key: ")
    device_id = get_android_device_id()
    result = check_license(license_key, device_id)

    if result['status'] != 'success':
        print(f"License verification failed: {result['message']}")
        sys.exit()

    print("License verified! Proceeding with adding user on Android/Linux...")

    print('Initializing Telegram client...')
    client = TelegramClient(str(session_name), api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    # Add user functionality here
    user_to_add = input("Enter the username or ID of the user to add: ")

    try:
        user = client.get_input_entity(user_to_add)
        client(functions.channels.InviteToChannelRequest(
            channel=target,
            users=[user]
        ))
        print(f"User {user_to_add} added successfully to the group on Android/Linux!")
    except Exception as e:
        print(f"Failed to add user {user_to_add}: {e}")

# Function to run the scraper for Windows
def run_scraper_windows():
    license_key = input("Enter your license key: ")
    device_id = get_windows_device_id()
    result = check_license(license_key, device_id)

    if result['status'] != 'success':
        print(f"License verification failed: {result['message']}")
        sys.exit()

    print("License verified! Proceeding with the scraper on Windows...")

    print('Initializing Telegram client...')
    client = TelegramClient(str(session_name), api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    print('Fetching Members...')
    all_participants = []

    # Fetch participants from the target group or channel
    try:
        all_participants = client.iter_participants(target, limit=None, filter=None, aggressive=True)
    except Exception as e:
        print(f"Error occurred while fetching participants: {e}")
        sys.exit()

    print('Saving to file...')
    with open("data_windows.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['sr. no.', 'username', 'user id', 'name', 'Status'])
        i = 0
        for user in all_participants:
            i += 1
            username = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([i, username, user.id, name, 'group name'])

    print('Members scraped successfully.')

# Function to run the scraper for Android/Linux
def run_scraper_android():
    license_key = input("Enter your license key: ")
    device_id = get_android_device_id()
    result = check_license(license_key, device_id)

    if result['status'] != 'success':
        print(f"License verification failed: {result['message']}")
        sys.exit()

    print("License verified! Proceeding with the scraper on Android/Linux...")

    print('Initializing Telegram client...')
    client = TelegramClient(str(session_name), api_id, api_hash)

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    print('Fetching Members...')
    all_participants = []

    # Fetch participants from the target group or channel
    try:
        all_participants = client.iter_participants(target, limit=None, filter=None, aggressive=True)
    except Exception as e:
        print(f"Error occurred while fetching participants: {e}")
        sys.exit()

    print('Saving to file...')
    with open("data_android.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['sr. no.', 'username', 'user id', 'name', 'Status'])
        i = 0
        for user in all_participants:
            i += 1
            username = user.username if user.username else ""
            first_name = user.first_name if user.first_name else ""
            last_name = user.last_name if user.last_name else ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([i, username, user.id, name, 'group name'])

    print('Members scraped successfully.')

# Main menu function
def main_menu():
    print("Choose an option:")
    print("1 - Get Device ID (Windows)")
    print("2 - Get Device ID (Android/Linux)")
    print("3 - Run Scraper (Windows)")
    print("4 - Run Scraper (Android/Linux)")
    print("5 - Add User (Windows)")
    print("6 - Add User (Android/Linux)")
    choice = input("Enter your choice (1, 2, 3, 4, 5, or 6): ")

    if choice == '1':
        device_id = get_windows_device_id()
        if device_id:
            print(f"Your Windows Device ID: {device_id}")
        else:
            print("Failed to retrieve Windows Device ID")
    elif choice == '2':
        device_id = get_android_device_id()
        if device_id:
            print(f"Your Android/Linux Device ID: {device_id}")
        else:
            print("Failed to retrieve Android/Linux Device ID")
    elif choice == '3':
        run_scraper_windows()
    elif choice == '4':
        run_scraper_android()
    elif choice == '5':
        add_user_windows()
    elif choice == '6':
        add_user_android()
    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")

if __name__ == "__main__":
    main_menu()