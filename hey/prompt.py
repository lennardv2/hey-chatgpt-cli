import hey.helpers
import sys
import termcolor
from termcolor import colored
from colorama import init
import os

# Array trick for passing by reference
current = [0]
waiter = ['.', '..', ' ', ' ', ' ', ' ']
has_yaml = False

def swallow_yaml(delayed_buffer, start = "[yaml]", end = "[\yaml]", name = "yaml", skip = False):
    global has_yaml

    delayed_buffer_joined = "".join(delayed_buffer)

    if start in delayed_buffer_joined:
        current[0] = 0
        flush_buffer = delayed_buffer_joined.replace(start, "")
        print(flush_buffer, end='', flush=True)
        
        print (colored("> Reading " + name + "  ", "green"), end="", flush=True)

        # Clear the buffer by reference
        delayed_buffer.clear()

        skip = True
        has_yaml = True

    if has_yaml == True:
        current[0] += 1
        cur = current[0]
        # Show the waiter in place
        print (colored("\b" + waiter[cur % len(waiter)], "green"), end="", flush=True)
        # print (colored(waiter[cur % len(waiter)], "green"), end="", flush=True)
        # print (colored(".", "green"), end="", flush=True)
    
    if end in delayed_buffer_joined:
        print()
        print()
        delayed_buffer.clear()
        skip = False
        has_yaml = False

    return skip


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
import sys

langs = ["python", "bash", "json", "javascript", "typescript", "html", "css", "php", "java", "c", "cpp", "csharp", "go", "rust", "swift", "kotlin", "ruby", "perl", "powershell", "sql", "shell", "dockerfile", "makefile", "ini", "toml", "xml", "diff", "markdown", "latex", "plaintext"]
current_lang = []

def swallow_code(delayed_buffer, start = "```", end = "```", lang = "python", skip = False):
    delayed_buffer_joined = "".join(delayed_buffer)

    if skip == True and end in delayed_buffer_joined:
        flush_buffer = delayed_buffer_joined.replace(end, "")

        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = TerminalFormatter()
        result = highlight(flush_buffer, lexer, formatter)

        print(result.strip(), end='', flush=True)

        delayed_buffer.clear()
        skip = False

        print()
        print("```")
        print()
      
        return skip

    if skip == False and start in delayed_buffer_joined:
        current[0] = 0
        flush_buffer = delayed_buffer_joined.replace(start, "")

        print(flush_buffer.strip(), end='', flush=True)

        print()
        print()
        print("```" + lang)
        
        # Clear the buffer by reference
        delayed_buffer.clear()

        skip = True

    return skip

def syntax_highlighter(delayed_buffer, skip = False):
    global current_lang

    current_lang_now = current_lang[0] if len(current_lang) > 0 else None

    if current_lang_now != None:
        langSkip = swallow_code(delayed_buffer, start = "```" + current_lang_now, end = "```", lang = current_lang_now, skip = skip)

        if langSkip == False:
            current_lang = []

        return langSkip
    else:
        for lng in langs:
            langSkip = swallow_code(delayed_buffer, start = "```" + lng, end = "```", lang = lng, skip = skip)

            if langSkip == True:
                current_lang.append(lng)
                return langSkip

    return skip

def parse_prompt(prompt_text, data = {}):
    ## Find the executing directory (e.g. in case an alias is set)
    ## So we can find the prompt.txt file
    home_path = os.path.expanduser("~")
    hey_path = os.path.join(home_path, ".hey")

    shell = os.environ.get("SHELL", "powershell.exe") 

    ## Load the prompt and prep it
    pre_prompt = prompt_text
    # pre_prompt = open(prompt_file,"r").read()
    pre_prompt = pre_prompt.replace("{shell}", shell)
    for key in data:
        pre_prompt = pre_prompt.replace("{"+key+"}", data[key])
    pre_prompt = pre_prompt.replace("{os}", hey.helpers.get_os_friendly_name())
    pre_prompt = pre_prompt.replace("{pwd}", os.getcwd())
    # Use puthon date functions
    pre_prompt = pre_prompt.replace("{datetime}", hey.helpers.get_datetime())

    prompt = pre_prompt

    return prompt