import os;
from hey.cli import read_prompt, set_start_prompt
script_path = os.path.dirname(os.path.realpath(__file__))

def load(hey):
    hey['commands']['chat'] = {
        "description": "This mode is just like using normal ChatGPT",
        "function": lambda: set_start_prompt("chat", read_prompt(script_path + "/prompt.txt")),
    }