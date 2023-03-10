#!/usr/bin/env python3
# http://zetcode.com/python/click/

import os
import platform
import openai
import sys
import subprocess
import distro
import re
import yaml

from termcolor import colored
from colorama import init

from termcolor import colored
from colorama import init

__author__ = "Lennard Voogdt"
__version__ = "1.0.0"
home_path = os.path.expanduser("~")  

def get_os_friendly_name():
  
  # Get OS Name
  os_name = platform.system()
  
  if os_name == "Linux":
      return "Linux/"+distro.name(pretty=True)
  elif os_name == "Windows":
      return os_name
  elif os_name == "Darwin":
     return "Darwin/macOS"

# Construct the prompt
def parse_prompt(prompt_file, data = {}):
  ## Find the executing directory (e.g. in case an alias is set)
  ## So we can find the prompt.txt file
  yolo_path = os.path.abspath(__file__)
  prompt_path = os.path.dirname(yolo_path)
  shell = os.environ.get("SHELL", "powershell.exe") 

  ## Load the prompt and prep it
  prompt_file = os.path.join(prompt_path, prompt_file)
  pre_prompt = open(prompt_file,"r").read()
  pre_prompt = pre_prompt.replace("{shell}", shell)
  for key in data:
    pre_prompt = pre_prompt.replace("{"+key+"}", data[key])
  pre_prompt = pre_prompt.replace("{os}", get_os_friendly_name())
  prompt = pre_prompt
  
  return prompt

def openai_classify(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You analyse the question and determine the best way to answer it."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=1000,
        stream=False
    )

    # Parse the yaml
    yaml_string = response["choices"][0]["message"]['content']

    output = yaml.safe_load(yaml_string)

    return output

messages = []

## Make above function fynamic based on watch_for length
## Import mute from above
def check_watch(delta_content, watch_for, watch_found, done, fail):
    all_false = [False for i in range(len(watch_for))]

    # Loop trough the watch_for list in reverse
    for i in range(len(watch_for)-1, -1, -1):
        checker = [True for x in range(i)] + [False for i in range(len(watch_for)-i)]

        if watch_found == checker:
            if delta_content.strip() == watch_for[i]:
                if (i == len(watch_for)-1):
                    done()
                watch_found[i] = True
                break
            else:
                if watch_found != all_false:
                    fail()
                    watch_found = all_false
                break
            


def openai_chat(message, assistant_message = None):
    if assistant_message:
        messages.append({"role": "assistant", "content": assistant_message})

    messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=1000,
        stream=True
    )

    buffer = ""

    swallow_file=["[y", "aml", "]", "file"]
    swallow_file_stream=[False, False, False, False]

    swallow_cmd=["[y", "aml", "]", "command"]
    swallow_cmd_stream=[False, False, False, False]

    # Holds every line that is not outputed because of detection of above
    swallowed=[]

    global failed; failed = [False, False]

    def on_file():
        print (colored("Receiving file: ", "blue"),end='')

    def on_command():
        print (colored("Receiving command: ", "green"),end='')
    
    def on_fail():
        global failed
        if failed[0] and failed[1]:
            # Spit it out it was false alarm
            for i in swallowed:
                print (i,end='')

            failed = [False, False]

    def on_file_fail():
        global failed
        failed[0] = True
        on_fail()
        # print (colored("Failed file", "red"),end='')

    def on_command_fail():
        global failed
        failed[1] = True
        on_fail()
        # print (colored("Failed command", "red"),end='')
    
    for chunk in response:
        # choices.delta.content
        delta=chunk["choices"][0]["delta"]

        if "content" in delta:
            delta_content = delta["content"]
        
            check_watch(delta_content, swallow_file, swallow_file_stream, on_file, on_file_fail)
            check_watch(delta_content, swallow_cmd, swallow_cmd_stream, on_command, on_command_fail)

            if swallow_cmd_stream[0] == False and swallow_file_stream[0] == False:
                print(delta_content,end='')
            else:
                swallowed.append(delta_content)

            buffer += delta["content"]

    return buffer

def get_question():
    # Parse arguments and make sure we have at least a single word
    if len(sys.argv) < 2:
        return None

    arguments = sys.argv[1:]

    return " ".join(arguments)

def run_command(command):
    print(command)
    print()
    print("[1] Run and exit (default)")
    print("[2] Run and continue")
    print("[3] Run and send to gpt")
    print("[4] Continue")
    print("[5] Exit")

    answer = input()
    # Check if y/Y or enter
    if answer == "" or answer == "1":
        print()
        subprocess.run(command, shell=True)
        exit()

    elif answer == "2":
        print()
        subprocess.run(command, shell=True)
        return None
    
    elif answer == "3":
        print()
        output = subprocess.run(command, shell=True, capture_output=True)
        print (output.stdout.decode("utf-8"))
        return output.stdout.decode("utf-8")

    elif answer == "4":
        return None

    elif answer == "5":
        exit()

def write_file(file, contents):
    print(file)
    print()
    print("[1] Save and exit (default)")
    print("[2] Save and continue")
    print("[3] Do not save and continue")
    print("[4] Exit")

    answer = input()


    # check for home ~ and replace it with the actual home path
    if file.startswith("~"):
        file = file.replace("~", home_path)

    if answer == "" or answer == "1":
        # Save and create if not exists
        with open(file, "w+") as f:
            f.write(contents)

        exit()

    elif answer == "2":
        # Save and create if not exists
        with open(file, "w+") as f:
            f.write(contents)

        return None

    elif answer == "3":
        return None

    elif answer == "4":
        exit()

def main(query = None):

    init()

    home_path = os.path.expanduser("~")    
    openai.api_key_path = os.path.join(home_path,".openai.apikey")

    user_input = get_question()

    if (user_input == None):
        print ("Hi! how can i help you?")
        print()
        print("You:", end=' ')
        user_input = input()
        print()

    # print("Question: " + user_input)

    chat_output = None
    prompt = None

    while(user_input != "exit" and user_input != "bye" and user_input != "quit"):
        if prompt == None:
            prompt = parse_prompt("prompt.start.txt", { 'question': user_input })

        chat_output = openai_chat(prompt, chat_output)

        yaml_output = re.search(r'\[yaml\](.*?)\[/yaml\]', chat_output, re.DOTALL)
        has_yaml = yaml_output != None

        if (has_yaml):
            yaml_response = yaml.safe_load(yaml_output.group(1))

            if "command" in yaml_response:
                command_output = run_command(yaml_response["command"])

                if command_output != None:
                    prompt = parse_prompt("prompt.command.txt", { 'output': command_output })
                    continue;

            if "file" in yaml_response:
                write_file(yaml_response["file"], yaml_response["contents"])


        print()
        print()
        print("You:", end=' ')
        user_input = input()
        print()

        prompt = parse_prompt("prompt.chat.txt", { 'question': user_input })
    exit()

if __name__ == "__main__":  
    main()