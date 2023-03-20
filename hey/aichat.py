import openai
import os
from hey.prompt import swallow_yaml
from hey.prompt import syntax_highlighter
import tiktoken

messages = [
    {"role": "system", "content": "You are called hey. You can help with questions about the command line, programming, or general questions."}
]

# Count tokens with tiktoken
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

def max_tokens():
    return 4096

def count_tokens(text):
    return len(encoding.encode(text))

def get_tokens(additional_tokens = ""):
    total = count_tokens(additional_tokens)
    for message in messages:
        total += count_tokens(message["content"])
    return total

def get_dollars(additional_tokens):
    return get_tokens(additional_tokens) / 1000 * 0.002

def get_tokens_available(additional_tokens = ""):
    return max_tokens() - get_tokens(additional_tokens)

def get_openai_key_path():
    home_path = os.path.expanduser("~")    
    return os.path.join(home_path,".openai.apikey")

def setup_openai_key():
    # detect if the key is already set (openai package read it by default)
    apikey = os.environ.get("OPENAI_API_KEY")
    if apikey:
        return True
    # if no key is set, try to read it from a file
    key = get_openai_key_path()
    openai.api_key_path = key
    return os.path.exists(key)

def clear():
    global messages
    messages.clear()
    messages = [
        {"role": "system", "content": "You are called hey. You can help with questions about the command line, programming, or general questions."}
    ]

def chat(message, assistant_message = None):
    if assistant_message:
        messages.append({"role": "assistant", "content": assistant_message})

    messages.append({"role": "user", "content": message})

    # print(messages)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
            max_tokens=1000,
            stream=True
        )
    except openai.error.InvalidRequestError as e:
        print()
        print("Error: " + str(e))
        print()
        print("You can reset the history with the command 'clear'")
        print()
        return ""

    output_buffer = ""
    delayed_buffer = []
    buffer_size = 5

    skip = False

    for chunk in response:
        # choices.delta.content
        delta=chunk["choices"][0]["delta"]

        if "content" in delta:
            delta_content = delta["content"]
            output_buffer += delta_content

            delayed_buffer.append(delta_content)

            # print (delta_content)
            skip = swallow_yaml(delayed_buffer, "[yaml:cmd]", "[/yaml:cmd]", "command", skip)
            skip = swallow_yaml(delayed_buffer, "[yaml:file]", "[/yaml:file]", "file", skip)
            skip = swallow_yaml(delayed_buffer, "[yaml:curl]", "[/yaml:curl]", "search request", skip)
            skip = swallow_yaml(delayed_buffer, "[yaml:lynx]", "[/yaml:lynx]", "search request", skip)
            skip = syntax_highlighter(delayed_buffer, skip)

            if skip == False and len(delayed_buffer) > buffer_size:
                print(delayed_buffer[0], end='', flush=True)
                # print_output(delayed_buffer[0])
                # remove first item of the buffer
                delayed_buffer.pop(0)
    
    # print_output("".join(delayed_buffer))
    print("".join(delayed_buffer), end='', flush=True)

    return output_buffer

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
import sys

highlight_buffer = ['']
highlight_index = 0
start_colorizing = False
# start_colorizing_line = 0
output_by_line = False

# items = ["It", " ", "is ", "a ", "beautiful ", "day ", "\n", "```", "python\n", "hello = 123", "``", "`\n", "Hmh"]
# items = ["It", " ", "is ", "a ", "beautiful ", "day ", "\n", "```", "python", "hello = 123", "``", "`\n", "Hmh"]

def print_output(output, finished=False):
    global highlight_buffer
    global highlight_index
    global start_colorizing
    global output_by_line
    # global start_colorizing_line

    if output == None:
        return

    def line_done(line):
        global output_by_line

        if output_by_line:
            print(line)

        if '```' in line:
            if not output_by_line:
                start_colorizing_line = highlight_index
                start_colorizing = True
                output_by_line = True
                # print()
                print(output, end='', flush=True)
            else:
                start_colorizing = False
                output_by_line = False
    

        if output_by_line:
            lexer = get_lexer_by_name("python", stripall=True)
            formatter = TerminalFormatter()
            result = highlight(line, lexer, formatter)
            # print (result, flush=True, end='')
            print (line, flush=True)
            # sys.stdout.write(result)


    # output = output.replace("\n", "xxx")
    if '\n' in output:
        ab = output.split("\n")

        print(ab)

        # loop over ab with key
        for i in range(len(ab) - 1):
            highlight_buffer[highlight_index] += ab[i]

            line_done(highlight_buffer[highlight_index])
            
            highlight_index += 1
            highlight_buffer.append('')
    else:
        highlight_buffer[highlight_index] += output
 
    if not output_by_line:
        print(output, end='', flush=True)

    if output_by_line and finished:
        print(highlight_buffer[highlight_index])
