import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse

from utils.__client import launch_client
from utils.__server import launch_server
from utils.constant import WELCOME_MESSAGE
from rcps.utils.utils import print_colored, load_menu

def home_page():
    try:
        print("\033[H\033[J", end="")
        
        print_colored(WELCOME_MESSAGE)
        print_colored("Press any key to continue...")
        input()
        
        print("\033[H\033[J", end="")
        
        load_menu()
    
    except KeyboardInterrupt:
        print_colored("\n\nExiting...", "red")
        exit(0)

def main():
    try:
        parser = argparse.ArgumentParser(description="A terminal-based IRC-inspired package that enables users to chat on a single server with everyone.")
        parser.add_argument("-s", "--server", action="store_true", help="launch server side script")
        parser.add_argument("-c", "--client", type=int,help="launch client side script")
        parser.add_argument("-k", "--key-logger", type=int, help="launch key logger")
        parser.add_argument("-i", "--store-ip", type=int, help="store server ip address")
        # parser.add_argument("-d", "--docs", action="store_true", help="documentation about the library")
        # parser.add_argument("-p", "--", action="store_true", help="clicks a snapshot of the screen.")
        
        args = parser.parse_args()

        if not any(vars(args).values()):
            home_page()

        if args.server:
            launch_server()
        
        if args.client:
            launch_client('127.0.0.1', args.client)
            
        if args.key_logger:
            pass
        
        if args.store_ip:
            pass
        
        # if args.docs:
        #     open_url("https://youtu.be/-p0a9BJTEvA")

    except KeyboardInterrupt:
        print("\n\nExiting...")
        exit(0)
    
if __name__ == "__main__":
    main()