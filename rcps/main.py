import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rcps.utils.base import StreamingServer, ScreenShareClient
from rcps.utils.__constant import WELCOME_MESSAGE, DOCS, DEFAULT_HOST, DEFAULT_PORT
from rcps.utils.utils import print_colored, load_menu, is_valid_ipv4_address, fetch_remote_ip
from rcps.utils.gui import launch_interface

def home_page():
    try:
        print("\033[H\033[J", end="")

        print_colored(WELCOME_MESSAGE)
        print_colored("[Press any key to continue...]")
        input()

        print("\033[H\033[J", end="")

        return load_menu()

    except KeyboardInterrupt:
        print_colored("\n\nExiting...", "red")
        exit(0)


def main():
    try:
        parser = argparse.ArgumentParser(description="This is rcps.")
        parser.add_argument("-s", "--server", action="store_true", help="launch server on target machine")
        parser.add_argument("-l", "--listen", action="store_true", help="listen to any live stream")
        parser.add_argument("-k", "--key-logger", action="store_true", help="launch key logger")
        parser.add_argument("-i", "--ipaddr", type=str, help="ipv4 address of the client")
        parser.add_argument("-p", "--port", type=int, help="port of the client")
        parser.add_argument("-d", "--docs", action="store_true", help="documentation about the tool")
        parser.add_argument("-g", "--gui", action="store_true", help="launch gui")

        args = parser.parse_args()

        if not any(vars(args).values()):
            response, args.ipaddr, args.port = home_page()
            
            if response in ["1", "2"]:
                print_colored("Starting server...", "blue")
                try:
                    print("\033[H\033[J", end="")
                    print_colored(
                        "Server started successfully at http://{}:{}".format(
                            args.ipaddr, args.port
                        ),
                        "green",
                    )
                    server = StreamingServer(
                        args.ipaddr, args.port, slots=4, quit_key="q"
                    )
                    server.start_server()
                except KeyboardInterrupt:
                    print_colored("\n\nExiting...", "red")
                    exit(0)

            elif response == "3":
                print_colored("Starting client...", "blue")
                try:
                    print("\033[H\033[J", end="")
                    screen_share_client = ScreenShareClient(
                        str(args.ipaddr), int(args.port), x_res=1024, y_res=576
                    )
                    screen_share_client.start_stream()
                except KeyboardInterrupt:
                    print_colored("\n\nExiting...", "red")
                    exit(0)

        if args.gui:
            launch_interface()
        
        elif args.key_logger:
            print("Key logger not implemented yet.")
            exit(0)

        elif args.docs:
            print(DOCS)

        if args.server or args.listen:
            if not args.ipaddr or not args.port:
                if args.server:
                    ipaddr, port = DEFAULT_HOST, DEFAULT_PORT
                elif args.listen:
                    ipaddr, port = fetch_remote_ip(), DEFAULT_PORT
            else:
                ipaddr, port = str(args.ipaddr).strip(), int(args.port)

            if not is_valid_ipv4_address(ipaddr):
                raise Exception(f"Invalid ipv4 address: {ipaddr}")

            if args.listen:
                server = StreamingServer(ipaddr, port, slots=4, quit_key="q")
                server.start_server()

            if args.server:
                screen_share_client = ScreenShareClient(ipaddr, port, x_res=1024, y_res=576)
                screen_share_client.start_stream()

    except KeyboardInterrupt:
        raise Exception("Exiting...")


if __name__ == "__main__":
    main()