import os;

from hey.cli import read_prompt, set_start_prompt
script_path = os.path.dirname(os.path.realpath(__file__))

def load(hey):
    hey['commands']['cli'] = {
        "description": "This allows for receiving commands, files and more",
        "function": lambda: set_start_prompt("cli", read_prompt(script_path + "/prompt.txt")),
    }