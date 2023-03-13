#!/usr/bin/env python3

import os
import sys

from termcolor import colored
import colorama

import hey.aichat
import importlib.metadata

from hey.prompt import parse_prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding.bindings.named_commands import accept_line
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from hey.install import install, load_plugins

# # items = ["It", " ", "is ", "a ", "beautiful ", "day ", "\n", "```", "python\n", "hello = 123", "``", "`\n", "Hmh"]
# items = ["It", " ", "is ", "a ", "beautiful ", "day ", "\n", "```", "python\n", "hello = 123", "``", "`\n", "Hmh"]

# for item in items:
#     hey.aichat.print_output(item)

# hey.aichat.print_output("", finished=True)

# exit()

prompt = None

home_path = os.path.expanduser("~")  
program_path = os.path.dirname(__file__)
user_path = home_path + "/.hey"

paths = {
    "chat_history" : user_path + "/chat_history",
    "commands_history" : user_path + "/commands_history",
    "log_file" : user_path + "/gpt_log.txt"
}

def prompt_path(name):
    # Check for the user_dir
    # Check ~/.hey/prompt/name.txt
    if os.path.exists(user_path + "/prompt/" + name + ".txt"):
        return user_path + "/prompt/" + name + ".txt"

    # Check ~/.hey/plugins/name/prompt.txt
    if os.path.exists(user_path + "/plugins/" + name + "/prompt.txt"):
        return user_path + "/plugins/" + name + "/prompt.txt"

    # Check program_path/prompt/name.txt
    if os.path.exists(program_path + "/prompt/" + name + ".txt"):
        return program_path + "/prompt/" + name + ".txt"

    # Check program_path/plugins/name/prompt.txt
    if os.path.exists(program_path + "/plugins/" + name + "/prompt.txt"):
        return program_path + "/plugins/" + name + "/prompt.txt"

    return paths['prompt_path'] + name + ".txt"

def read_prompt(path):
    return open(path,"r").read()

app_state = {
    "log_mode": False,
    "start_prompt": read_prompt(prompt_path("cli")),
}

session = PromptSession(history=FileHistory(paths["chat_history"]))
cmd_session = PromptSession(history=FileHistory(paths["commands_history"]))

__author__ = importlib.metadata.metadata("hey-gpt")['Author']
__version__ = importlib.metadata.version("hey-gpt")

def get_initial_arguments():
    # Parse arguments and make sure we have at least a single word
    if len(sys.argv) < 2:
        return None

    arguments = sys.argv[1:]

    return " ".join(arguments)

def help():
    print(colored("Hey version " + __version__, "green"))
    print ("ChatGPT on the commandline")
    print()

    # loop over commands with Keys
    for key, value in commands.items():
        print(colored(key, 'green'), end='')
        print(" " * (20 - len(key)), end='')
        print(value['description'])

def exit():
    print("Bye!")
    sys.exit()

def clear():
    global prompt
    prompt = None
    hey.aichat.clear()

    print("ChatGPT history reset")

def log_mode():
    app_state["log_mode"] = not app_state["log_mode"]

    if app_state["log_mode"] == True:
        print("log_mode mode is now on")
        print("Logfile is located at " + paths["log_file"])

    else:
        print("log_mode mode is now off")

def log(text):
    if text != None and app_state["log_mode"] == True:
        # Append to the file and create of nopt exists
        file = open(paths["log_file"], "a")

        file.write(text)
        file.close()

def show_log():
    if app_state["log_mode"] == True:
        file = open(paths["log_file"], "r")
        print(file.read())
        file.close()

# def set_start_prompt(mode):

def mode(mode):
    if (mode == "cli"):
        set_start_prompt("cli", read_prompt(prompt_path("cli")))

    elif (mode == "chat"):
        set_start_prompt("chat", read_prompt(prompt_path("chat")))

def set_start_prompt(mode, prompt_text):
    clear()
    app_state["start_prompt"] = prompt_text
    print("You are now in " + mode + " mode.")

def clear_history():
    # Clear history
    file = open(paths["chat_history"], "w")
    file.close()

    file = open(paths["commands_history"], "w")
    file.close()

    print("Hey history cleared on disk")

def run_custom(command = ""):
    from hey.parse import parse_output
    command = cmd_session.prompt("Command: ", default=command)

    if command == "exit" or "":
        return

    output = """
    [yaml:cmd]
        command: """ + command + """
    [/yaml:cmd]
    """

    return parse_output(output)
    # Run the command

def last_ran_command_from_history(index = -2):
    import os

    if os.name == 'posix':  # for Linux/Unix/MacOS
        # Check if zsh is the default shell
        if os.environ.get('SHELL') == '/bin/zsh':
            history_file = os.path.expanduser("~/.zsh_history")
        else:
            history_file = os.path.expanduser("~/.bash_history")
    elif os.name == 'nt':  # for Windows
        history_file = os.path.expanduser('%userprofile%' + "/AppData/Roaming/Microsoft/Windows/PowerShell/PSReadline/ConsoleHost_history.txt")

    with open(history_file, 'r') as f:
        lines = f.readlines()

    last_command = lines[index].strip()

    if last_command.startswith("hey"):
        return last_ran_command_from_history(index - 1)

    if os.environ.get('SHELL') == '/bin/zsh':
        last_command = last_command.split(";")[1]
    
    return last_command

commands = {
    "help": {
        "description": "Show this help",
        "function": help
    },
    "reinstall": {
        "description": "Reinstall the default prompts",
        "function": lambda: install(True)
    },
    "log": {
        "description": "Toggle log_mode mode",
        "function": log_mode
    },
    "run": {
        "description": "Run a system command and send the response to ChatGPT",
        "function": run_custom
    },
    "clear": {
        "description": "Reset the chat, clear the tokens",
        "function": clear
    },
    "clear history": {
        "description": "Reset the hey command-line history",
        "function": clear_history
    },
}



def you_input():
    style = Style.from_dict({'': '#59acfb','you': '#59acfb',})
    msg = [('class:you', '❯❯ ')]
    print()

    def get_rprompt():
        text = session.default_buffer.text
        return 'Tokens: ' + str(hey.aichat.get_tokens(text)) + "/" + str(hey.aichat.max_tokens())

    user_input = session.prompt(msg, rprompt=get_rprompt, style=style, cursor=CursorShape.BEAM, auto_suggest=AutoSuggestFromHistory())

    return user_input

def main():
    from hey.parse import parse_output
    global prompt
    colorama.init()

    hey.aichat.find_openai_key()

    user_input = get_initial_arguments()

    if (user_input == None):
        print("Hi! How can I help you?")
        user_input = you_input()

    chat_output = None

    while(user_input != "exit" and user_input != "bye" and user_input != "quit"):
        # Trim user_input
        user_input = user_input.strip()

        if user_input == "":
            user_input = you_input()
            continue

        if user_input in commands:
            send_response = commands[user_input]["function"]()

            if send_response != None and send_response.strip() != "":
                prompt = send_response
            else:
                user_input = you_input()
                continue

        if (user_input == "last"):
            last_command = last_ran_command_from_history()

            if (last_command != None and last_command.strip() != ""):
                print()
                print("I must rerun your last command to see it's output")
                print()
                send_response = run_custom(last_command)

                if send_response != None and send_response.strip() != "":
                    prompt = send_response
                else:
                    user_input = you_input()
                    continue

        if prompt == None:
            prompt = parse_prompt(app_state["start_prompt"], { 'question': user_input })

        print()

        chat_output = hey.aichat.chat(prompt, chat_output)

        log(prompt)
        log(chat_output)
        
        send_response = parse_output(chat_output)

        if send_response.strip() != "":
            prompt = send_response
            continue
            
        print()

        user_input = you_input()

        prompt = parse_prompt(read_prompt(prompt_path("question")), { 'question': user_input })
    exit()

loaded_plugins = []

def init():
    try:
        hey.install.install()
        # load_plugins(commands)
        loaded_plugins = load_plugins({
                'app_state': app_state,
                'commands': commands,
            },
        )
        main()
    except KeyboardInterrupt:
        print()
        exit()

if __name__ == "__main__":  
    init()