import os

def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt_continue() -> bool:
    print("\nPress enter to continue or type 'quit' to exit:")
    return input("> ").strip().lower() != "quit"


def welcome_message():
    print(r"""
╔════════════════════════════════════════════════════╗
║               Welcome to ROMsHelper!               ║
║                   Version 0.1.0                    ║
║====================================================║   
║                                                    ║      
║           A simple Command Line tool for           ║
║               organizing your ROMs.                ║
║                                                    ║
║====================================================║                      
║ > For more information consult the Github page:    ║
║ https://github.com/Malagel/ROMs-Helper             ║                                                          
╚════════════════════════════════════════════════════╝
""")