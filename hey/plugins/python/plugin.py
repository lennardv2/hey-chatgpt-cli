import os;

script_path = os.path.dirname(os.path.realpath(__file__))

def load(hey):
    set_mode = hey['set_mode']

    # Load the plugin
    hey['commands']['python'] = {
        "description": "Python expert prompt",
        "function": lambda: set_mode("python", script_path + "/prompt.txt"),
    }
