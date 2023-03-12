import os;

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from hey.cli import read_prompt, set_start_prompt
from hey.prompt import parse_prompt

home_path = os.path.expanduser("~")  
user_path = home_path + "/.hey"

script_path = os.path.dirname(os.path.realpath(__file__))
session = PromptSession(history=FileHistory(user_path + "/lang_history"))

def set_lang():
    language = session.prompt("Enter a language: ")

    prompt = parse_prompt(read_prompt(script_path + "/prompt.txt"), {
        "language": language
    })

    set_start_prompt(language, prompt)


def load(hey):
    hey['commands']['lang'] = {
        "description": "Set the prompt to a specific language",
        "function": set_lang
    }
