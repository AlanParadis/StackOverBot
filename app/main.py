
import os
from dotenv import load_dotenv
import discord
#from stackoverbot import StackOverBot
import time

#todo : Setting Up Logging for better debug

def main():
    #get parent folder path
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #get env folder
    env_path = os.path.join(parent_path, 'env\\.env')
    # Load the .env file
    load_dotenv(env_path)

    # Get the debug guild id from the .env file
    debug_guild = os.getenv("DISCORD_DEBUG_GUILD")
    # Create the bot
    if(debug_guild):
        bot = discord.Bot(debug_guilds=[debug_guild])
    else:
        bot = discord.Bot()

    # Get the bot token
    token = os.getenv("DISCORD_TOKEN")
    if(token == None):
        assert("Missing token environenment variable")

    bot.load_extension("cogs.stackoverbot")

    # Run the bot
    bot.run(token)


if(__name__ == "__main__"):
    main()