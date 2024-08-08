import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse

from rcps.utils.base import StreamingServer, ScreenShareClient
from rcps.utils._constant import WELCOME_MESSAGE, DOCS
from rcps.utils.utils import print_colored, load_menu, is_valid_ipv4_address


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
        parser = argparse.ArgumentParser(
            description="A terminal-based IRC-inspired package that enables users to chat on a single server with everyone."
        )
        parser.add_argument(
            "-s", "--server", action="store_true", help="launch server side script"
        )
        parser.add_argument(
            "-c", "--client", action="store_true", help="launch client side script"
        )
        parser.add_argument(
            "-k", "--key-logger", action="store_true", help="launch key logger"
        )
        parser.add_argument(
            "-i", "--ipaddr", type=str, help="ipv4 address of the client"
        )
        parser.add_argument("-p", "--port", type=int, help="port of the client")
        parser.add_argument(
            "-d", "--docs", action="store_true", help="documentation about the library"
        )

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

        if args.key_logger:
            print("Key logger not implemented yet.")
            exit(0)

        # if args.store_ip:
        #     print("IP address not stored yet.")
        #     exit(0)

        if args.docs:
            print(DOCS)

        if not args.ipaddr or not args.port:
            raise Exception(f"""
                Please provide the ip address and port.\n\n
                {DOCS}
            """)

        ipaddr, port = str(args.ipaddr).strip(), int(args.port)

        if not is_valid_ipv4_address(ipaddr):
            print(ipaddr)
            raise Exception("Invalid ipv4 address.")

        if args.server:
            server = StreamingServer(ipaddr, port, slots=4, quit_key="q")
            server.start_server()

        if args.client:
            screen_share_client = ScreenShareClient(ipaddr, port, x_res=1024, y_res=576)
            screen_share_client.start_stream()

    except KeyboardInterrupt:
        raise Exception("Exiting...")


if __name__ == "__main__":
    main()
