import openai
import os
from hey.prompt import swallow_yaml
import tiktoken

messages = []

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

def get_tokens_available(additional_tokens = ""):
    return max_tokens() - get_tokens(additional_tokens)

def find_openai_key():
    home_path = os.path.expanduser("~")    
    openai.api_key_path = os.path.join(home_path,".openai.apikey")

def clear():
    messages.clear()

def chat(message, assistant_message = None):
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

            if skip == False and len(delayed_buffer) > buffer_size:
                print(delayed_buffer[0], end='', flush=True)
                # remove first item of the buffer
                delayed_buffer.pop(0)
    
    print("".join(delayed_buffer), end='', flush=True)

    return output_buffer
