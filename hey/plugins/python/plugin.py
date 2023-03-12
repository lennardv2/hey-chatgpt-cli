import os;

from hey.cli import read_prompt, set_start_prompt
script_path = os.path.dirname(os.path.realpath(__file__))

def load(hey):
    # Load the plugin
    hey['commands']['python'] = {
        "description": "Python expert prompt",
        "function": lambda: set_start_prompt("python", read_prompt(script_path + "/prompt.txt")),
    }
