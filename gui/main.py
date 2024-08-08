# import threading
import customtkinter
from PIL import Image
from pyperclip import copy
from rcps.utils.base import StreamingServer, ScreenShareClient
from rcps.utils.utils import get_code, is_valid_ipv4_address

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# stop_listening_event = threading.Event()

def connect_button_function():
    # stop_listening_event.set()
    ipaddr = enter_code.get().strip()
    if is_valid_ipv4_address(ipaddr):
        screen_share_client = ScreenShareClient(ipaddr, port=2907, x_res=1024, y_res=576)
        screen_share_client.start_stream()

def copy_code_function():
    code = get_code()
    copy(code)

def start_listening(ipaddr="0.0.0.0", port=2907):
    server = StreamingServer(ipaddr, port, slots=4, quit_key="q")
    server.start_server()


app = customtkinter.CTk()

app.title('RCPS : Remote Control Panel')
app.iconbitmap('favicon.ico')
app.geometry("250x380")

logo = Image.open("./logo.png")
logo_image = customtkinter.CTkImage(logo, size=(100, 36))
logo_image_label = customtkinter.CTkLabel(app, text="", image=logo_image)
logo_image_label.grid(row=0, column=0, pady=40, sticky="ew")

enter_code = customtkinter.CTkEntry(master=app, placeholder_text="Enter Client's Code", width=160)
enter_code.grid(row=1, column=0, pady=10, padx=45, sticky="ew")

your_code = customtkinter.CTkLabel(master=app, text="Your code: {}".format(get_code()))
your_code.grid(row=2, column=0, pady=10, padx=45, sticky="ew")

copy_code = customtkinter.CTkImage(Image.open("./temp.png"), size=(16, 16))
image_button = customtkinter.CTkButton(master=app, text="", image=copy_code, width=22, command=copy_code_function)
image_button.grid(row=3, column=0, pady=10, padx=45, sticky="ew")

connect = customtkinter.CTkButton(master=app, text="Connect", command=connect_button_function)
connect.grid(row=4, column=0, pady=10, padx=45, sticky="ew")

listen = customtkinter.CTkButton(master=app, text="Listen", command=start_listening)
listen.grid(row=5, column=0, pady=10, padx=45, sticky="ew")

app.mainloop()