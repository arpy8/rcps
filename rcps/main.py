import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse

from rcps.utils.base import StreamingServer, ScreenShareClient
from rcps.utils._constant import WELCOME_MESSAGE
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
        parser.add_argument("-s", "--server", action="store_true",  help="launch server side script")
        parser.add_argument("-c", "--client", action="store_true",  help="launch client side script")
        parser.add_argument("-k", "--key-logger", action="store_true", help="launch key logger")
        parser.add_argument("-i", "--ipaddr", type=str, help="ipv4 address of the client")
        parser.add_argument("-p", "--port", type=int, help="port of the client")
        # parser.add_argument("-d", "--docs", action="store_true", help="documentation about the library")
        
        args = parser.parse_args()

        if not any(vars(args).values()):
            home_page()

        if args.server:
            if not args.ipaddr or not args.port:
                print_colored("Please provide the ip address and port.\n\nExample usage:\n\nrcps -s -i 192.168.1.100 -p 8888", "red")
                exit(0)
                
            ipaddr, port = str(args.ipaddr).strip(), int(args.port)
            
            if  len([i for i in ipaddr.split(".") if i.isdigit()]) != 4:
                print_colored("Invalid ip address.", "red")
                exit()
            
            if 0 > port > 65535:
                print_colored("Invalid port.", "red")
                exit()
            
            server = StreamingServer(ipaddr, port, slots=4, quit_key='q')
            server.start_server()
        
        if args.client:
            if not args.ipaddr or not args.port:
                print_colored("Please provide the ip address and port.\n\nExample usage:\n\nrcps -c -i 192.168.1.100 -p 8888", "red")
                exit(0)
                
            ipaddr, port = str(args.ipaddr).strip(), int(args.port)
            
            if  len([i for i in ipaddr.split(".") if i.isdigit()]) != 4:
                print_colored("Invalid ip address.", "red")
                exit()
            
            if 0 > port > 65535:
                print_colored("Invalid port.", "red")
                exit()
            
            screen_share_client = ScreenShareClient(ipaddr, port, x_res=1024, y_res=576)
            screen_share_client.start_stream()
        
        if args.key_logger:
            pass
        
        # if args.store_ip:
        #     pass
        
        # if args.docs:
        #     open_url("https://youtu.be/-p0a9BJTEvA")

    except KeyboardInterrupt:
        print("\n\nExiting...")
        exit(0)
    
if __name__ == "__main__":
    main()