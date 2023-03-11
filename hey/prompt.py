import hey.helpers
import termcolor
from termcolor import colored
from colorama import init
import os

# Array trick for passing by reference
current = [0]
waiter = ['.', '..', ' ', ' ', ' ', ' ']

def swallow_yaml(delayed_buffer, start = "[yaml]", end = "[\yaml]", name = "yaml", skip = False):
    delayed_buffer_joined = "".join(delayed_buffer)

    if start in delayed_buffer_joined:
        current[0] = 0
        flush_buffer = delayed_buffer_joined.replace(start, "")
        print(flush_buffer, end='', flush=True)
        
        print (colored("> Reading " + name + "  ", "green"), end="", flush=True)

        # Clear the buffer by reference
        delayed_buffer.clear()

        skip = True

    if skip == True:
        current[0] += 1
        cur = current[0]
        # Show the waiter in place
        print (colored("\b" + waiter[cur % len(waiter)], "green"), end="", flush=True)
        # print (colored(waiter[cur % len(waiter)], "green"), end="", flush=True)
        # print (colored(".", "green"), end="", flush=True)
    
    if end in delayed_buffer_joined:
        print()
        print()
        delayed_buffer.clear()
        skip = False

    return skip

def parse_prompt(prompt_file, data = {}):
    ## Find the executing directory (e.g. in case an alias is set)
    ## So we can find the prompt.txt file
    home_path = os.path.expanduser("~")
    hey_path = os.path.join(home_path, ".hey")

    shell = os.environ.get("SHELL", "powershell.exe") 

    ## Load the prompt and prep it
    pre_prompt = open(prompt_file,"r").read()
    pre_prompt = pre_prompt.replace("{shell}", shell)
    for key in data:
        pre_prompt = pre_prompt.replace("{"+key+"}", data[key])
    pre_prompt = pre_prompt.replace("{os}", hey.helpers.get_os_friendly_name())
    pre_prompt = pre_prompt.replace("{pwd}", os.getcwd())
    # Use puthon date functions
    pre_prompt = pre_prompt.replace("{datetime}", hey.helpers.get_datetime())

    prompt = pre_prompt

    return prompt