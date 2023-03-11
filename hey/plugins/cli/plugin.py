import os;

script_path = os.path.dirname(os.path.realpath(__file__))

def load(hey):
    hey['commands']['cli'] = {
        "description": "This allows for receiving commands, files and more",
        "function": lambda: hey['set_mode']("cli", script_path + "/prompt.txt"),
    }