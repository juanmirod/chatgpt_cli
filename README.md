# ChatGPT CLI

This is a command line interface that uses OpenAI's GPT API to simulate chat with various personalities. The interface is written in Python and requires an OpenAI API key to function. The objective with this tool is to have an easy and fast communication way with ChatGPT (no need for browser, captcha, login, etc) and to have more control on the parameters and the output.

The interface includes a feature that allows the user to finish and save the conversation:
When the user writes `q` as request, the script finishes the conversation and stores the entire conversation as a markdown file in the `history` folder.

The chat now allow multiline entries for the user (needed when you copy and paste some code) do to send
the request the user needs to finish with a `*` as termination character. The termination character can
be configured when instantiating the ChatGPT class, if `None` is passed the user request will be send on return. 

It also includes a couple of example system prompts that define a "character" to follow for ChatGPT.

## Dependencies

All dependencies are listed in the `requirements.txt` file. To install dependencies, it's recommended to use a virtual environment such as venv.

### Setting up a Virtual Environment

To create a virtual environment for the project, run the following command:

```python3 -m venv local```

This will create a virtual environment called `local` in your project directory.

Next, activate the virtual environment using the command:

```source local/bin/activate```

This will activate the virtual environment and any packages you install will be installed locally instead of globally.

To install the required dependencies for the project, run:

```pip install -r requirements.txt```

### Using the ChatGPT CLI

Before running the chat, you need to set the `API_KEY` environment variable to your OpenAI API key. You can either set this variable in your working environment, or use a `.env` file in the project directory.

To start the chat, run the following command:

```python3 start.py```

There are several sample personalities provided in the repo, which can be run simply by specifying the name of the file:

```python3 pythonExpert.py```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Possible new features that would be interesting:

- [x] Implement ReAct pattern for fact checking and arithmetic
- [] add more actions
- [] Load a history file to continue a conversation
- [x] Copy and paste code in the request (broken because of new lines)
- [] Publish a conversation as a gist or somewhere else

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.

## Contributors

Based in the a sample project by Max Woolf ([@minimaxir](https://minimaxir.com))
ChatGPT contributed to develop this repo.

