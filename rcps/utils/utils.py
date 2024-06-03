from termcolor import colored
from utils.constant import _BANNER

def print_colored(text, color='green'):
    print(colored(text, color))
    
def load_menu():
    print_colored(f"""
    {_BANNER}    
    
    1. Start Server
    2. Start Client
    3. Key Logger
    4. Capture Screen
    5. Store IP
    6. Exit
    
    """)
    
    user_choice = input("-> ")
    
    return user_choice