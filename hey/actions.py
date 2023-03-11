import hey.aichat
import os
import subprocess
home_path = os.path.expanduser("~")  
from simple_term_menu import TerminalMenu
from termcolor import colored
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from hey.cli import cmd_session
import sys

def run(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    capture_errors = ""
    capture_output = ""

    while True:
        output = process.stdout.readline().decode(sys.stdout.encoding)
        if output == "" and process.poll() is not None:
            break
        if output:
            capture_output += output
            print(output.strip())

    while True:
        error = process.stderr.readline().decode(sys.stdout.encoding)
        if error == "" and process.poll() is not None:
            break
        if error:
            capture_errors += error

    if capture_output.strip() == "":
        print(colored(capture_errors, "red"))

    return capture_output, capture_errors

def run_command(command, dangerous):
    options = ["Run", "Change", "Skip", "Run and exit", "Exit"]

    if dangerous:
        options = ["Skip", "Change", "Run (dangerous)", "Run and exit (dangerous)", "Exit"]

    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()

    if dangerous:
        if index == 0:
            index = 2
        elif index == 2:
            index = 0

    # Run
    if index == 0:
        print()

        output, errors = run(command)

        return output, errors

    # Skip
    elif index == 1:
        command = cmd_session.prompt("Command: ", default=command)

        return run_command(command, False)

    # Skip
    elif index == 2:
        return None, None

    # Run and exit
    elif index == 3:
        print()

        run(command)

        exit()

    elif index == 4:
        exit()

def ask_run_through_gpt(response):
    print (colored("Do you want to send the response to chatgpt? (" + str(hey.aichat.count_tokens(response)) + "/" + str(hey.aichat.get_tokens_available()) + " tokens)", "blue"))
    print()

    options = ["No", "Yes", "Exit"]

    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()

    # Yes
    if index == 1:
        return True

    if index == 2:
        exit()

    return False

def write_file(file, contents):
    def save_file(file, contents):
        style = Style.from_dict({'': '#59acfb','you': '#59acfb',})
        msg = [('class:you', 'You: ')]

        file = prompt("Save file? (clear to discard) ", default=file, style=style)

        if file == "":
            return

        if file.startswith("~"):
            file = file.replace("~", home_path)

        # Check if file exists
        if os.path.exists(file):
            print()
            print("File already exists. Overwrite?")
            overwrite = ["No", "Yes"]

            terminal_menu2 = TerminalMenu(overwrite)
            index2 = terminal_menu2.show()

            if index2 == 0:
                return

        with open(file, "w+") as f:
            f.write(contents)
        
        print()
        print("File saved to " + file)

    save_file(file, contents)

def run_curl(curl_command, dangerous):
    return run_command(curl_command, dangerous)


    