# Hey Chatbot

Hey is a powerful chatbot for the command line that uses ChatGPT to generate commands based on natural language input.

### Command mode
This uses a prompt with your os and shell included. It can send commands for you to run (or skip). It will show when a command is concidered dangerous, the default will be to skip the command.
https://user-images.githubusercontent.com/168357/224721506-abbb4887-1d17-497c-9148-c9e592e60f22.mp4

### Help
<img width="791" alt="help" src="https://user-images.githubusercontent.com/168357/224721572-c1167661-463b-4354-8dcb-3f4e90f18b99.png">

### Lang mode:
The lang mode can help with programming questions in specific language.
https://user-images.githubusercontent.com/168357/224721527-0718dea4-a332-4417-bb71-ccaf14616ad4.mp4

### Chat
In chat mode you have a quite normal chatgpt experience in your command line, with the option to save parts to a file.
https://user-images.githubusercontent.com/168357/224721549-52e45014-b7d1-4ee7-a368-d120baedb2ca.mp4

## Installation
Pipx is a tool that allows you to install and run Python packages in isolated environments. This means that you can install Hey without worrying about conflicting dependencies or affecting other Python packages on your system.

To install Hey via pipx, you can use the following command:
```
pipx install hey-gpt
```
Once Hey is installed, you can run it from anywhere on your system by typing `hey` in your terminal.

(see pipx https://pypa.github.io/pipx/)

## Usage

```
hey
```
To use Hey, simply type in your question or command and Hey will start a chat session and generate commands. It always asks to confirm before execution.

(More will follow...)

```
hey (command)
```
This will immediatly question chat gpt with your question and show a response. The sessions will remain active until you type ``bye`` or ``exit``.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
