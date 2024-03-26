# bot_anime 
[PythonAnywhere](http://zaryana.pythonanywhere.com/)
## My inspiration 
[Я люблю аниме🦊🍥🍜](https://youtu.be/s914hB2Ei0A?si=u9zA_WgYJ6Svv_aF)

*If you'd be interested to know what I was inspired to make bot_anime from, check it out.*

## Description

**bot_anime** — provides information about *techniques* from the anime "Naruto" including details about which episode they first appeared in, as well as information about the techniques' characteristics. Additionally, the bot collects statistics on the *top_10 techniques* by counting the number of user requests for techniques and automatically updates the graph data. 
## Installation
Create and activate a virtual environment, install the required libraries:
```bash
pip install -r requirements.txt
```
## Files 
**bot.py** — main bot file (*bot's head, dispatch center*) сontains code for processing user messages, interacting with Telegram platform APIs.
____
### Supplement:

Additionally, in the main file there is a variable that belongs to a special class **Dispatcher** `dp = bot.dispatcher`. The work of this object can be compared to the work of a **telephonist**. The task of the dispatcher is to process incoming requests (*calls*) and direct them to the appropriate handlers (*subscribers*). Therefore, we can say that in a Telegram bot's dispatcher can *fulfill the role of a telephonist*, receiving messages from users and directing them to the appropriate handlers for responding to these messages.
____

**config.py** — сontains settings such as a token to authenticate to the Telegram API and a SQLALCHEMY_DATABASE_URI to connect to the database (*in this file **token** value will be empty*).

**dp.py** — creates a connection to the database, creates a session for executing queries and defines a base class for models (description of an empty database). 

**handlers.py**  — file (*brain file, bot's brain*) that stores all functions that are intercepted by handlers (CommandHandler, MessageHandler...etc).
___

### Supplement:

**def add_user** — the function for adding a new user to the database, if there is no user in the database.

**def greet_user** — the function that greets the user at command (*/start*) 

**def send_plot** — the function to send the user a graph showing the top_10 techniques by number of requests. 

**def show_techs** — the function to display the available techniques for a specified episode.

**def show_tech_info** — the function for displaying information about the technique selected by the user.
____

**models.py** — description of tables about **users** and **techniques** in the database. 

**naruto_parser.py** — goes to the given site (https://jut.su/by-episodes/), parses it and loads all the received information about the techniques into the database.

**utils.py** — is used to create and customize keyboards.

**database.db** — contains two tables, one stores information about the users, the other contains all information about the techniques.

## Creating your own bot

To create your own working bot based on these files, you need to follow these steps:

1. Execute the "Installation" section.
2. Create your bot using BotFather and obtain your unique token.
3. Insert the value of your token into the `TOKEN` variable in the `config.py` file.
4. Run the bot (`bot.py`).

You don't need to use `naruto_parser.py` because you have already gathered all the information about techniques in the `database.dp` file. However, if you wish, you can skip downloading the database file and run the parser to collect your own database.

## How to use the bot_anime (*bot operation*)
*Here's my own bot:*
[*Я люблю аниме*](https://t.me/ha2004rembot)

Here's a video where you can see exactly how it works:

<video controls width="400" height="400" src="наруто.MP4" title="Title"></video>


https://github.com/zaryana223/bot_anime_project/assets/113456045/e7008d99-71c5-4c02-b857-5745d7d83f95


## Used libraries

*python-telegram-bot==13.4* — for developing bot_anime on the Telegram platform using Python.

*requests==2.31.0* — allows to send requests to servers and receive responses.

*tqdm==4.66.2* — is used to create a progress bar in a loop.

*matplotlib==3.8.3* — for data visualization.

*bs4==0.0.2* — provides a simple way to extract information from HTML documents. 






