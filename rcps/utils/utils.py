import json
import requests
import subprocess
from termcolor import colored
from rcps.utils.__constant import _BANNER, DEFAULT_HOST, DEFAULT_PORT, IP_STORE_API, BEARER_TOKEN


def print_colored(text, color="green"):
    print(colored(text, color))

def update_remote_ip():
    device_ip = get_device_ip()

    response = requests.post(
        f"{IP_STORE_API}/set-ip",
        json={"ip": device_ip},
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
    )
    
    return json.loads(response.text)["status"] == "success"

def fetch_remote_ip():
    response = requests.get(
        f"{IP_STORE_API}/get-ip",
        headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
    )
    response = json.loads(response.text)

    if response["status"] == "success":
        return response["ip"]
    else:
        return None

def get_device_ip():
    response = subprocess.run(['ipconfig'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    response = response.split("IPv4 Address")[-1].split('\n')[0].strip('\r').split(':')[-1].strip()
    return response

def is_valid_ipv4_address(ip):
    parts = ip.strip().split('.')
    return (len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts))

def load_menu():
    while 1:
        print("\033[H\033[J", end="")
        print_colored(f"""{_BANNER}
            1. Start Server ({DEFAULT_HOST}:{DEFAULT_PORT})
            2. Start Server (Specify IP and Port)
            3. Start Client
            4. Key Logger
            5. Capture Screen
            6. Store IP
            7. Exit
            """)

        user_choice = input("-> ")

        if user_choice == "1":
            print("\033[H\033[J", end="")
            return user_choice, DEFAULT_HOST, DEFAULT_PORT

        elif user_choice == "2":
            ipaddr = input("Enter IP Address: ")

            if not ipaddr:
                print_colored("Invalid IP Address.", "red")
                continue

            port = input("Enter Port: ")

            if not port:
                print_colored("Invalid Port.", "red")
                continue

            print("\033[H\033[J", end="")
            return user_choice, ipaddr, port

        elif user_choice == "3":
            ipaddr = input("Enter IP Address: ")

            if not ipaddr:
                print_colored("Invalid IP Address.", "red")
                continue

            port = input("Enter Port: ")

            if not port:
                print_colored("Invalid Port.", "red")
                continue

            print("\033[H\033[J", end="")
            return user_choice, ipaddr, port

        elif user_choice == "4":
            print("Key logger not implemented yet.")
            input()

        elif user_choice == "5":
            print("Capture screen not implemented yet.")
            input()

        elif user_choice == "6":
            print("Store IP not implemented yet.")
            input()

        elif user_choice == "7":
            exit(0)

        else:
            print_colored("Invalid choice.", "red")
            continue

if __name__ == "__main__":
    print(fetch_remote_ip())