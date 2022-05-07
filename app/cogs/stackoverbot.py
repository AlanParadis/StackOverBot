import os
import discord
from discord import ApplicationContext, Option
from discord.ext import commands
import urllib.request
import asyncio
import json
import gzip

class StackOverBot(discord.Cog):

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready!")

    @commands.slash_command(name = "search", description = "Perfom a search on stackoverflow")
    async def search(self, ctx : ApplicationContext,
    search : Option(str, description= "What you would like to search for", required=True),
    tags : Option(str,description= "Semicolon separated tags", required=True),
    sort : Option(str, description= "Sort method of the search", choices=["activity", "votes", "creation", "relevance"], required = False, default="votes"),
    min : Option(str,description= "Minimum value for the search sorting method", required=False,default=0)):
        #await ctx.defer()

        # Get author of the search command
        searchAuthor = ctx.author

        if sort != "relevance":
            min = "&min=" + str(min)
        else:
            min = ""

        # Fill the url of the satckoverflow api with the search
        base_url = "https://api.stackexchange.com/2.3/search?page=1&pagesize=5&order=desc{}&sort={}&tagged={}&site=stackoverflow".format(
            min, sort, tags)
        # Format the url
        base_url = urllib.parse.quote(base_url, safe="/:=?&")
        search_url = "&intitle={}".format(urllib.parse.quote(search, safe=''))
        url = base_url + search_url
        # Send request to the api and get the data
        page = urllib.request.urlopen(url)
        html = page.read()
        html = gzip.decompress(html)
        html = html.decode("utf-8")
        data = json.loads(html)

        loop = True
        index = 0
        while(loop):
            # Get questions list
            items = data['items']
            # If list if empty, break the loop
            if(len(items) == 0):
                await ctx.response.send_message("<@{}>\nSorry, can't find any questions :confused:".format(searchAuthor.id))
                loop = False
                return
            # Get the current question
            question = items[index]
            link = question["link"]
            # reponse message to send
            message_str = "Here we are <@{}> \n{}".format(searchAuthor.id, link)
            # Send a response if it's the first time, send a folowup if it's not
            if(index == 0) :
                # Show the question
                interaction = await ctx.response.send_message(message_str)
                # convert the interaction to a message
                message = await interaction.original_message()
            else:
                message = await ctx.followup.send(message_str)
            # get emoji and add it as a reaction
            emoji = '⏭'
            await message.add_reaction(emoji)
            
            # Define your check
            # Checks if the reaction author is the author of the message
            # and if the reaction emoji is '⏭'
            def check(_reaction, user):
                return user == searchAuthor and str(_reaction.emoji) == emoji

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
            # That way the bot doesn't wait forever for a reaction
            except asyncio.TimeoutError:  
                print("Ran out of time, interaction ended")
                loop = False
                return
            if reaction:
                # 'if statement' is regarded if the given reaction is valid (and not None)
                print("Received reaction")
                if(index + 1 < len(items)):
                    index = index + 1
                else:
                    await ctx.followup.send("Sorry, that's all I can get :robot_face:")
                    loop = False
                    return


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(StackOverBot(bot)) # add the cog to the bot
