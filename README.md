# ChatGPT CLI

![Badge for the testing action](https://github.com/juanmirod/chatgpt_cli/actions/workflows/python-app.yml/badge.svg)

This is a command line interface that uses OpenAI's GPT API to simulate chat with various personalities. The interface is written in Python and requires an OpenAI API key to function. The objective with this tool is to have an easy and fast communication way with ChatGPT (no need for browser, captcha, login, etc) and to have more control on the parameters and the output.

The interface includes a feature that allows the user to finish and save the conversation:
When the user writes `q` as request, the script finishes the conversation and stores the entire conversation as a markdown file in the `history` folder.

The chat now allow multiline entries for the user (needed when you copy and paste some code) do to send
the request the user needs to finish with a `*` as termination character. The termination character can
be configured when instantiating the ChatGPT class, if `None` is passed the user request will be send on return. 

It also includes a couple of example system prompts that define a "character" to follow for ChatGPT.

## Run it with docker

If you have docker in your machine and just want to run the default personality (JARVIS, a helpful AI assistant created by Tony Stark) you can run:

```

# build the container
docker build -t jarvis .

# Run the container as a command line app
docker run --rm -it jarvis

```

## Run without docker, using virtual environment
### Setting up a Virtual Environment

To create a virtual environment for the project, run the following command:

```
python3 -m venv local
```

This will create a virtual environment called `local` in your project directory.

Next, activate the virtual environment using the command:

```
source local/bin/activate
```

This will activate the virtual environment and any packages you install will be installed locally instead of globally.

To install the required dependencies for the project, run:

```
pip install -r requirements.txt
```

### Using the ChatGPT CLI

Before running the chat, you need to set the `API_KEY` environment variable to your OpenAI API key. You can either set this variable in your working environment, or use a `.env` file in the project directory.

To start the chat, run the following command:

```
python3 characters/start.py
```

There are several sample personalities provided in the repo, which can be run simply by specifying the name of the file:

```
python3 characters/psycologist.py
```

To create a new character, copy any of the characters files and modify the system prompt as you like, you can try some prompts from here: https://prompts.chat

I also have an alias in my laptop and another one in termux to run the prompt with one simple command:

```
alias jarvis='cd ~/jarvis && source local/bin/activate; python3 characters/termux.py'
```

## Features

- [x] Save the conversation
- [x] Ask for a summary in a few words to name the file of the saved conversation
- [x] Error handling: the bot answers with the error message 
- [x] Implement ReAct pattern for fact checking and arithmetic
- [x] Copy and paste code in the request: It waits for a termination character so you can write several lines as part of your volley.
- [x] Works on Termux! \o/
- [x] Dockerfile to run the app from a docker container
- [x] Autosave
- [x] Add an action to generate images with the help of ChatGPT using Dall-e API
  
## I'm working on...

- [ ] Long term memory with a vector database

## Possible next features, cool things that I would like...

- [ ] Load a history file to continue a conversation
- [ ] Summarize the conversation in a paragraph when it's getting to the token limit to be able to continue on track
- [ ] Publish a conversation as a gist or somewhere else
- [ ] Multi-agent generation with several specialized agents

## Runing the test suite

This repo uses pytest for the test suite, to run it run:

```
pytest
```

Running the tests in watch mode:

```
ptw
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.

## Contributors

Based in the a sample project by Max Woolf ([@minimaxir](https://minimaxir.com))
ChatGPT contributed to develop this repo.

