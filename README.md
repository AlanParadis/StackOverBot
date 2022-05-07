
# StackOverBot 🤖

A discord bot to search Stack Overflow questions

Written in Python 3.9

## 👀
![](https://i.ibb.co/VWXPGW5/image-2022-05-07-202341359.png)
![](https://i.ibb.co/PG68bZm/image-2022-05-07-002807207.png)

*Click the ⏭ to show the next question !*

**Bot token can be stored in separated `.env` file in a `env` folder at the root of the repository**

# Docker 🐋

Build image using : 
```
$    docker build stackoverbot .
```
Run container using : 
```
$   docker run \
    -d --restart unless-stopped \
    -e DISCORD_TOKEN="your_token" \
    -e DISCORD_DEBUG_GUILD="guild_debug_id" \
    --name container_name \
    stackoverbot
```
⚠ `DISCORD_DEBUG_GUILD` is not mandatory (This is to update the bot only in the specified server, avoiding to wait for change propagation)

# 
Comunication with the discord API with : [Pycord](https://github.com/Pycord-Development/pycord)

License : [DBAD](https://github.com/philsturgeon/dbad)
