from termcolor import colored
from rcps.utils._constant import _BANNER

def print_colored(text, color='green'):
    print(colored(text, color))
    
def load_menu():
    while 1:
        print("\033[H\033[J", end="")
    
        print_colored(f"""{_BANNER}    
            1. Start Server
            2. Start Client
            3. Key Logger
            4. Capture Screen
            5. Store IP
            6. Exit
            """)
            
        user_choice = input("-> ")
        
        if user_choice != "":
            return user_choice