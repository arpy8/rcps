import os
import customtkinter
from PIL import Image
from rcps.utils.base import StreamingServer, ScreenShareClient
from rcps.utils.utils import fetch_remote_ip


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def path(file):
    return os.path.join(os.path.dirname(__file__), "../assets/", file)
    
def launch_target(ipaddr="0.0.0.0", port=2907):
    server = StreamingServer(ipaddr, port, slots=4, quit_key="q")
    server.start_server()
    
def launch_host(ipaddr=fetch_remote_ip(), port=2907):
    client = ScreenShareClient(ipaddr, port=port, x_res=1024, y_res=576)
    client.start_stream()

def launch_interface():
    app = customtkinter.CTk()

    app.title('RCPS : Remote Control Panel')
    app.iconbitmap(path('favicon.ico'))
    app.geometry("240x200")

    logo = Image.open(path("logo.png"))
    logo_image = customtkinter.CTkImage(logo, size=(100, 26))
    logo_image_label = customtkinter.CTkLabel(app, text="", image=logo_image)
    logo_image_label.grid(row=0, column=0, pady=20, sticky="ew")

    connect = customtkinter.CTkButton(master=app, text="Launch Target Server", command=launch_target)
    connect.grid(row=1, column=0, pady=10, padx=45, sticky="ew")

    listen = customtkinter.CTkButton(master=app, text="Watch Stream", command=launch_host)
    listen.grid(row=2, column=0, pady=10, padx=45, sticky="ew")

    app.mainloop()