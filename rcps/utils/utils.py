import subprocess
from termcolor import colored
from rcps.utils._constant import _BANNER, DEFAULT_HOST, DEFAULT_PORT


def print_colored(text, color="green"):
    print(colored(text, color))


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
            ipaddr = input("Enter IP Address: ")

            if not ipaddr:
                print_colored("Invalid IP Address.", "red")
                continue

            port = input("Enter Port: ")

            if not port:
                print_colored("Invalid Port.", "red")
                continue

            return user_choice, ipaddr, port

        elif user_choice == "2":
            return user_choice, DEFAULT_HOST, DEFAULT_PORT

        elif user_choice == "3":
            ipaddr = input("Enter IP Address: ")

            if not ipaddr:
                print_colored("Invalid IP Address.", "red")
                continue

            port = input("Enter Port: ")

            if not port:
                print_colored("Invalid Port.", "red")
                continue

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


def _run_command(command):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            command,
            startupinfo=startupinfo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=True,
            text=True,
        ).stdout.read()
        return str(process) + "\n"

    except subprocess.CalledProcessError as e:
        return f"Error: {e}"


def get_ips():
    command = ["ipconfig", "|", "findstr", "/i", "ipv4"]
    ip = _run_command(command)

    return [i.split(":")[1].strip() for i in ip.split("\n") if i != ""]


if __name__ == "__main__":
    print(get_ips())
