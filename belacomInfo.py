import colorama
from datetime import datetime

# initialisation
colorama.init()

# get timestamp
timestamp = datetime.now().astimezone().strftime("[%Y-%m-%d %H:%M:%S] ")

def info(info):
    print(timestamp + colorama.Fore.LIGHTGREEN_EX + "[INFO] "+colorama.Fore.RESET+info)

def warning(warning):
    print(timestamp + colorama.Fore.LIGHTYELLOW_EX + "[WARNING] "+colorama.Fore.RESET+warning)

def error(error):
    print(timestamp + colorama.Fore.RED + "[ERROR] "+colorama.Fore.RESET+error)