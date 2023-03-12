import hey.actions
from prompt_toolkit import prompt
import re
import yaml
from hey.prompt import parse_prompt
from termcolor import colored
from hey.cli import prompt_path
from hey.cli import read_prompt

def print_header(title, index, length, type="Command", dangerous = False):
    show_num = "(" + str(index + 1) + "/" + str(length) + ") "
    if (length == 1):
        show_num = ""

    print()
    print(show_num + type + ": " + colored(title, "green"))

    if(dangerous):
        print(colored("WARNING: This can be dangerous!", "red"))

    print()

def parse_output(chat_output):
    print()
    yaml_output = re.findall(r'\[yaml:.*?\](.*?)\[\/yaml:.*?\]', chat_output, re.DOTALL)

    response = ""

    # loop over yaml_output with index
    for index, yaml_command in enumerate(yaml_output):
        # parse the yaml
        try:
            yaml_response = yaml.safe_load(yaml_command)
        except yaml.YAMLError as exc:
            print(colored(exc, "red"))

            yaml_command = prompt("Please fix the YAML: ", default=yaml_command)

            try:
                yaml_response = yaml.safe_load(yaml_command)
            except yaml.YAMLError as exc:
                print(colored(exc, "red"))

                return response

        dangerous = False

        if "dangerous" in yaml_response:
            dangerous = yaml_response["dangerous"]

        # check if the yaml has a command
        if "command" in yaml_response:
            command = yaml_response["command"]
            print_header(command, index, len(yaml_output), "Command", dangerous)

            # run the command
            command_output, command_errors = hey.actions.run_command(command, dangerous)

            print()

            output = ""

            if command_output != None and command_output.strip() != "":
                output += command_output

            if command_errors != None and command_errors.strip() != "":
                output += command_errors

            # print(output)

            # check if the command has output
            if output != None and output.strip() != "":
                run_throught_gpt = hey.actions.ask_run_through_gpt(output)

                if (run_throught_gpt == True):
                    response += parse_prompt(read_prompt(prompt_path("command")), { 'command': command, 'output': output })

        # check if the yaml has a file
        if "file" in yaml_response:
            file = yaml_response["file"]

            # write the file
            print_header(file, index, len(yaml_output), "File", dangerous)

            hey.actions.write_file(yaml_response["file"], yaml_response["contents"])

        # if "curl" in yaml_response:
        #     curl = yaml_response["curl"]
        #     print_header(curl, index, len(yaml_output), "Curl", dangerous)

        #     command_output = actions.run_curl(curl, dangerous)

        #     # Do a GET request to the url with curl
        #     # check if the command has output
        #     if command_output != None and command_output.strip() != "":
        #         print (command_output)
        #         print()
        #         run_throught_gpt = actions.ask_run_through_gpt(command_output)

        #         if (run_throught_gpt == True):
        #             response += parse_prompt(prompt_path("command"), { 'command': curl, 'output': command_output })


    return response