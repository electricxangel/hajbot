import os
import random
from discord import app_commands
import praw as praw
import discord
from dotenv import load_dotenv
import datetime
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw



file = open("sharkpics", "r")   #opens file with shark file paths
possible_images = []
hajpics = file.readlines()  #reads lines

for haj in hajpics:
    possible_images.append(haj.replace("\n", ""))   #appends all shark file paths to possible_images
file.close()

file = open("affirmations", "r")   #opens file with affirmations
possible_affirmations = []
affirmations = file.readlines()  #reads lines

for affirmation in affirmations:
    possible_affirmations.append(affirmation.replace("\n", ""))   #appends all affirmations to possible_affirmations
file.close()



load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
embed = discord.Embed() #initialise embed


class hajbot(discord.Client):   #hajbot
    def __init__(self):
        super().__init__(intents=discord.Intents.all()) #initialises hajbot
        self.synced = False

    async def on_ready(self):
        print("servers hajbot is in:")  #prints all servers hajbot is in
        for server in bot.guilds:
            print("• " + str(server))

        await self.wait_until_ready()
        if not self.synced: #checks if commands already synced
            await tree.sync()   #syncs commands
            self.synced = True


bot = hajbot()  #assigns hajbot to variable

tree = app_commands.CommandTree(bot)    #initialise command tree


def addtext(text):       #function to add text to images + scale text. used in later commands
    global imgtoopen
    imgtoopen = random.choice(possible_images)
    img = Image.open(f"imgs/{imgtoopen}")  # opens image
    draw = ImageDraw.Draw(img)  # creates ImageDraw object
    font = ImageFont.truetype("C:\Windows\Fonts\ARLRDBD.TTF", 1000)  # sets font

    while font.getlength(text=text) >= 1000:  # loop makes font smaller until it fits on the image
        font.size -= 1
        fontsize = font.size
        font = ImageFont.truetype("C:\Windows\Fonts\ARLRDBD.TTF", fontsize)  # sets the font to be the right size

    font = ImageFont.truetype("C:\Windows\Fonts\ARLRDBD.TTF", fontsize)
    draw.text((0, 0), text, (255, 255, 255), font=font, stroke_width=25, stroke_fill=(0, 0, 0))  # draws text onto image
    img.save("imgs/haj_image.jpg")  # saves image

    file_to_send = discord.File(rf"imgs/haj_image.jpg")
    return file_to_send




@tree.command(name="blahaj", description="send a random shork") #start of blahaj command
async def blahaj(interaction: discord.Interaction):
    file = random.choice(possible_images)   #chooses random blahaj image
    x = discord.File(rf"imgs/{file}")   #converts image to discord.File type
    await interaction.response.send_message(file=x) #sends image file


    # writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write("at " + str(current_time) + ": blahaj, sent " + str(
        file) + ", requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()



@tree.command(name="servercount", description="how many servers hajbot is in")  #start of servercount command
async def servercount(interaction: discord.Interaction):
    await interaction.response.send_message("hajbot is in " + str(len(bot.guilds)) + " servers!")   #sends length of bot.guilds (aka amount of servers hajbot is in)


    # writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write(
        "at " + str(current_time) + ": servercount, requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()



@tree.command(name="commandlist", description="sends a list of hajbot's commands")  #start of commandlist command
async def commandlist(interaction: discord.Interaction):
    await interaction.response.send_message("LIST OF COMMANDS:\n\n"     #sends full list of hajbot's commands
                            "•blahaj: generates a random shork image\n"
                            "•servercount: sends number of servers HajBot is currently in\n"
                            "•reddit: sends random post from r/blahaj \n"
                            "•commandlist: displays list of commands\n"
                            "•affirmation: sends a random haj affirmation\n"
                            "•texthaj: add text to a random picture of blahaj\n"
                            "•about: sends link to HajBot's carrd\n\n"
                            "more commands coming soon to an IKEA near you!")



    # writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write(
        "at " + str(current_time) + ": commandlist, requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()



@tree.command(name="reddit", description="sends a post from r/blahaj")  #start of reddit command
async def reddit(interaction: discord.Interaction):

    reddit_api = praw.Reddit(client_id='',        #creates reddit api and signs in
                             client_secret='',
                             user_agent='HajBot')
    all_subs = []   #initialises list of submissions to randomly select


    for submission in reddit_api.subreddit("blahaj").new(limit=50): #iterates through r/blahaj submissions
        all_subs.append(submission) #appends each submission to all_subs


    random_sub = random.choice(all_subs)    #choose random submission
    name = random_sub.title
    url = random_sub.url


    while "https://www.reddit.com/gallery/" in random_sub.url:  #filters out links that don't work
        random_sub = random.choice(all_subs)    #picks random submission
        name = random_sub.title
        url = random_sub.url


    embed = discord.Embed(title=name, color=discord.Color.blue())   #creates embed
    embed.set_image(url=url)
    embed.set_footer(text=url)


    await interaction.response.send_message(embed=embed)    #sends embedded post


    # writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write("at " + str(current_time) + ": reddit, sent " + str(
        url) + ", requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()


@tree.command(name="about", description="sends hajbot's carrd") #start of about command
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("ABOUT HAJBOT: \n\n"
                           "https://hajbot.carrd.co/")

    #writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write("at " + str(current_time) + ": about, requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()



@tree.command(name="serverlist", description="sends names of all servers hajbot is in") #start of serverlist command
async def serverlist(interaction: discord.Interaction):
    message = "servers hajbot is in:\n\n"   #begins making message


    for server in bot.guilds:   #loops through all servers hajbot is in
        message = message + "• " + str(server) + "\n"   #appends server name to message
    await interaction.response.send_message(message)    #sends full list of servers


    # writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write("at " + str(current_time) + ": serverlist, requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()



@tree.command(name="texthaj", description="add text to a blahaj")   #start of texthaj command
async def texthaj(interaction: discord.Interaction, text: str):

    await interaction.response.send_message(file=addtext(text=text))  #sends file in a message


    #writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write("at " + str(current_time) + ": texthaj, sent " + str(imgtoopen) + " with text: " + text + ", requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()

@tree.command(name="affirmation", description="send an affirming message for if you're having a bad day ♡")
async def affirmation(interaction: discord.Interaction):

    affirmation = random.choice(possible_affirmations)  #chooses affirmation from list

    await interaction.response.send_message(file=addtext(affirmation))


    #writes to activity log
    log = open("activity_log", "a")
    current_time = datetime.datetime.now()
    message_author = interaction.user.name
    channel = interaction.channel
    log.write("at " + str(current_time) + ": affirmation, sent " + affirmation + ", requested by: " + message_author + " in " + str(channel) + "\n")
    log.close()

# @bot.event
# async def on_message(message, ctx):
#     if message.content == "nuke":
#         for guild in bot.guilds:
#             if guild.id == 1092582737652744212:




hajbot.run(bot, token=DISCORD_TOKEN)    #starts hajbot