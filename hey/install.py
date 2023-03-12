import os
import glob
from prompt_toolkit import prompt

from hey.aichat import find_openai_key
from termcolor import colored

def install(force=False):
    # and copy them to ~/.hey/
    home_path = os.path.expanduser("~")
    hey_path = os.path.join(home_path, ".hey")
    prompt_path = os.path.join(hey_path, "prompt")
    program_path = os.path.dirname(__file__)

    # Check for openai key
    openai_key_path = os.path.join(home_path, ".openai.apikey")

    if not os.path.exists(openai_key_path):
        print(colored("* No OpenAI key found at " + openai_key_path, 'light_grey'))

        api_key = prompt("Please enter your OpenAI key: ")
        with open(openai_key_path, "w") as f:
            f.write(api_key)

    find_openai_key()

    if not os.path.exists(hey_path):
        print(colored("* Creating " + hey_path, 'light_grey'))
        os.makedirs(hey_path)

    # if not os.path.exists(prompt_path):
    #     # print(colored("* Creating " + prompt_path, 'light_grey'))
    #     os.makedirs(prompt_path)

    # # Get all the prompt.* files in the directory of this script
    # files = glob.glob(os.path.join(program_path, "prompt/*"))

    # for file in files:
    #     # If file doesnt exist, copy it with shutil
    #     if not os.path.exists(os.path.join(prompt_path, os.path.basename(file))) or force:
    #         print(colored("* Creating " + prompt_path + "/" + os.path.basename(file), 'light_grey'))
    #         shutil.copy(file, prompt_path)

    # In the program_path are plugins that we want to copy to ~/.hey/plugins
    # The plugins are in a subdirectory each
    # plugins_path = os.path.join(program_path, "plugins")
    # plugins = glob.glob(os.path.join(plugins_path, "*"))

    # for plugin in plugins:
    #     plugin_name = os.path.basename(plugin)
    #     plugin_path = os.path.join(hey_path, "plugins", plugin_name)

    #     if not os.path.exists(plugin_path):
    #         print(colored("* Creating " + plugin_path, 'light_grey'))
    #         os.makedirs(plugin_path)

    #     # Copy all files in the plugin directory
    #     files = glob.glob(os.path.join(plugin, "*"))

    #     for file in files:
    #         if not os.path.exists(os.path.join(plugin_path, os.path.basename(file))) or force:
    #             print(colored("* Creating " + plugin_path + "/" + os.path.basename(file), 'light_grey'))
    #             shutil.copy(file, plugin_path)

loaded_plugs = []

def load_plugins(data):
    # Load plugins
    home_path = os.path.expanduser("~")
    hey_path = os.path.join(home_path, ".hey")
    program_path = os.path.dirname(__file__)

    output = []

    load_plugins_in_directory(data, hey_path)
    load_plugins_in_directory(data, program_path)

    return output

def load_plugins_in_directory(data, path):
    # Load plugins
    home_path = os.path.expanduser("~")
    plugins_path = os.path.join(path, "plugins")

    # Get all the plugin.* directories in the directory of this script
    plugins = glob.glob(os.path.join(plugins_path, "*"))

    output = []

    # Load all plugins
    # They each have a plugin.py file with a load() function
    for plugin in plugins:
        plugin_name = os.path.basename(plugin)

        if plugin_name in loaded_plugs:
            continue
        
        loaded_plugs.append(plugin_name)

        plugin_path = os.path.join(plugins_path, plugin_name)

        # Check if plugin.py exists
        if not os.path.exists(os.path.join(plugin_path, "plugin.py")):
            continue

        import importlib.util
        spec = importlib.util.spec_from_file_location("plugin", os.path.join(plugin_path, "plugin.py"))
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)

        output.append(plugin.load(data))

    return output