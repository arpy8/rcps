import socket
import pydirectinput as pg
from pynput.keyboard import Listener

from rcps.utils.key_maps import convert_key_to_str, convert_key
from rcps.utils.constant import DEFAULT_HOST, \
                                DEFAULT_PORT, \
                                CLIENT_HOST, \
                                CLIENT_PORT


class Base:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.listener = None
    
    def start_server(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
        """
        Start the server socket to listen for incoming connections.
        
        Parameters
        ----------
        host : str, optional
            The hostname to bind the server to. Defaults to '0.0.0.0'.
        port : int, optional
            The port number to bind the server to. Defaults to 2907.      
            
        Note: Use ipconfig(windows) or ifconfig(linux) to find the ipv4 address of the host.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((host, port))
            self.server_socket.listen()
            print(f"Server listening on {host}:{port}")
            
            self.client_socket, _ = self.server_socket.accept()
            print("Client connected")
            
            def show(key):
                self.key_str = convert_key_to_str(key)
                self.client_socket.send(self.key_str.encode('utf-8'))
                    
            with Listener(on_press=show) as self.listener:
                self.listener.join()

            self.server_socket.close()
            self.client_socket.close()
            return "Connection closed"
        
        except KeyboardInterrupt:
            self.client_socket.close()
            return "Connection closed"
        
    def start_client(self, host: str = CLIENT_HOST, port: int = CLIENT_PORT) -> str:
        """
        Start the client socket and connect to the server.
        
        Parameters
        ----------
        host : str
            The hostname of the server to connect to.
        port : int, optional
            The port number of the server to connect to. Defaults to 2907.
            
        Note: The port number should be the same as the server port number.
        """
        if host is None:
            return "Please provide a hostname to connect to"
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            self.done = False

            while not self.done:
                try:
                    self.key = self.client_socket.recv(1024).decode('utf-8')
                    self.key_ = convert_key(self.key)
                    
                    print(self.key, self.key_)
                    
                    if self.key_ == 'Key.esc':
                        self.done = True
                    
                    if self.key_ is not None:
                        pg.press(self.key_)
                    
                except Exception as e:
                    print(e)
                
            self.client_socket.close()
            return "Connection closed"
            
        except KeyboardInterrupt:
            self.client_socket.close()
            return "Connection closed"
            

if __name__ == "__main__":
    base = Base()
    # base.start_server()
    base.start_client("192.168.1.4", 2907)