import os;

script_path = os.path.dirname(os.path.realpath(__file__))

def load(hey):
    hey['commands']['chat'] = {
        "description": "This mode is just like using normal ChatGPT",
        "function": lambda: hey['set_mode']("chat", script_path + "/prompt.txt"),
    }