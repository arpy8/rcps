import socket
import pydirectinput as pg 
from convertor import convert_key
 
        
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

done = False

while not done:
    try:
        key = client.recv(1024).decode('utf-8')
        key_ = convert_key(key)
        
        print(key, key_)
        
        if key_ == 'Key.esc':
            done = True
        
        if key_ is not None:
            pg.press(key_)
        
    except Exception as e:
        print(e)
    
client.close()