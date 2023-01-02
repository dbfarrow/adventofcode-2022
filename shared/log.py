
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKYELLOW = '\033[33m'
    OKGREEN = '\033[92m'
    OKCYAN = '\033[36m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LogContext:

    def __init__(self):
        self.debug = False

context = LogContext()

def trace(msg):
    if context.debug and context.trace:
        print(f'{bcolors.OKCYAN}[ ] {msg} {bcolors.ENDC}')

def debug(msg):
    if context.debug:
        print(f'{bcolors.OKCYAN}[%] {msg} {bcolors.ENDC}')

def info(msg):
    print(f'{bcolors.OKYELLOW}[+] {msg}{bcolors.ENDC}')

def warn(msg):
    print(f'{bcolors.WARNING}[-] {msg}{bcolors.ENDC}')

def success(msg):
    print(f'{bcolors.OKGREEN}[*] {msg}{bcolors.ENDC}')

def failure(msg):
    print(f'{bcolors.FAIL}[!] {msg}{bcolors.ENDC}')
