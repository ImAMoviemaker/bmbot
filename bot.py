"""
Blackmagic Design Discord Community bot
Version 1.0.0
Written by TimothyLH
With additions by Dave Caruso

ChangeLog:
v1.0.0
Introduces a basic set of functions
"""
#Import Libraries and Env-Variables
import os
import random
import psutil
import discord
import urllib
import re
from dotenv import load_dotenv

#Import Custom Code
from bmd_crawler.interface import allVisibleResolveVersionNames,getResolveVersionData,getResolveLatestData,allResolveVersionNames,allVisibleFusionVersionNames,getFusionVersionData,getFusionLatestData,allFusionVersionNames
from functions import channel_help
from const import *

print('Trying to start')

#Load Bot Token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
HELP = os.getenv('CHANNEL_HELP')
TERMINAL = os.getenv('CHANNEL_TERMINAL')
print(GUILD)


#Create bot
from discord.ext import commands

bot = commands.Bot(command_prefix='!bmd ')

#--- START UP CODE ---------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord! Discord.py Version: {discord.__version__}')
    print('Currently running at CPU: {0} RAM: {1}'.format(psutil.cpu_percent(), psutil.virtual_memory()[2]))

    await bot.change_presence(activity=discord.Game(name='DaVinci Resolve'))


#--- Welcome Message -------------------------------------------------------------------------------------------------------------------------------------------
@bot.event
async def on_member_join(member):
    await bot.get_channel(479770860601737216).send(
        '{0} {1.mention}, welcome to the Blackmagic Community! Please read the {2}. Type _!bmd help_ and _!bmd channels_ to get a quick introduction'
        .format(discord.utils.get(bot.get_guild(479297254528647188).emojis, name='bmd'),
        member,
        bot.get_channel(479298119255851029).mention)
    )
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Blackmagic Community! Please note that we use diffrent channels for diffrent things, you can see an overview below:'
    )
    embed = discord.Embed(title="Channel Overview", description="See what each channel is for below:", color=0xff8000)
    embed.set_footer(text="Contact Staff for more informations")
    embed.add_field(name="#general", value=f"Talk about anything related to Filmmaking and DaVinci Resolve. Pretty much anything not matching the other channels can be discussed here")
    embed.add_field(name="#davinci-resolve-help", value=f"Ask questions about DaVinci Resolve and Related Software (Fusion, Fairlight...) in here")
    embed.add_field(name="#show-off-your-work", value=f"Finished a new video? Have a clip you made and love? Share them in here! You are allowed to post links to the video/still from other plattforms")
    embed.add_field(name="#show-off-your-gear", value=f"Have you bought a new camera? Built a new epic rig? Cinemoded your loved lenses? Share them here")
    embed.add_field(name="#grade-my-still", value=f"Have a Clip/Still you like and would like to get some diffrent views on grading it? Share it in here. Attach a BRAW or other high-quality file!")
    embed.add_field(name="#bot-commands", value=f"Want to interact with one of our bots? Please paste them in here. Please only use _!bmd rule_ outside this channel")
    embed.add_field(name="#off-topic", value=f"Got something to share that is not related to Blackmagic or you have a funny meme? In here please")
    await member.dm_channel.send(embed=channel_help())

#--- PING PONG -------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name="ping", description="Use this command to see if the bot is online")
async def on_command(ctx):
    replays = [
        "Pong!", "No! I'm better than just writting 'Pong'", "Pong... ee. Hah you didn't expect this one. No seriously get yourself a warm blanket, it's cold outside!", "Stop pinging me! I want to sleep", "Dude stop pinging me! I'm presenting the new Blackmagic Not Anymore Pocket Cinema Camera 8k",
        f"Better ping gooogle than me. My current ping to Google is: {random.randint(1,10)}", "You expected me to say Pong! And so I did...", f"Pingreeeeee {discord.utils.get(bot.get_guild(479297254528647188).emojis, name='PeepoPing')}",
        "Ping? Ping! I will tell you who I ping next!", "Ping, Pong, Ping, Pong, Ping, Pong, Ping, Pong... That's the last Ping Pong Championship summarized", "Ping!", "async def ping(ctx):\n    await ctx.channel.send('Pong')"
    ]
    await ctx.channel.send(random.choice(replays))

#--- Rules -----------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='rule', help='Displays the selected rule. Do not give a number to get a general warning. Give a username to warn a specific user.')
async def on_command(ctx, id: int):
    if id == 1:
        msg = '1️⃣ Respect other users and their opinions. No impersonation. No racism, sexism, transphobia, homophobia, etc. Your race does not give you a pass to say slurs freely. Rules apply to everyone!'
    elif id == 2:
        msg = '2️⃣ We are a filmmaking discord, not a debate club. Please keep controversy about politics, religion, etc. out of here.'
    elif id == 3:
        msg = '3️⃣ English is the universal standard language.  Any sort of conversation in a foreign language is strictly prohibited. Most of our staff speak English so its not easy to tell if you\'re breaking the rules in another language. Violation of this could end on a mute or warning.'
    elif id == 4:
        msg = '4️⃣ No spamming of any kind. Please be polite to other users and do not be disruptive. Includes but is not limited to nicknames, text, emoji, links, images, EXCESSIVE CAPS, censor dodging (eg. use of spoilers), and spam mentioning @ role/user. Do not pointlessly ping Official Blackmagic Design Staff members for questions others can answer.'
    elif id == 5:
        msg = '5️⃣ Content sharing is allowed.\nPost your work in {0} \nPost your gear in {1} \nKeep memes in {2} strictly.'.format(bot.get_channel(479297477590384665).mention, bot.get_channel(479297610851811329).mention, bot.get_channel(654069173831335937).mention)
    elif id == 6:
        msg = '6️⃣ No loopholes. A loophole is when you try to find technicalities in the rules so you don\'t get punished for what you did.  If you ever find any loopholes then report them to a staff member to be fixed.  Loopholes will not be tolerated and are strictly prohibited.'
    elif id == 7:
        msg = '7️⃣ Keep all your drama out of this server. If you have any sort of an issue with another member then you can simply block them and move on or make an attempt at making amends in private messages (DMs).  Anywhere but this server is the place for you to do this. Violation of this rule will most likely lead to a mute or ban.'
    else:
        msg = '⚠️ Please follow the rules. You can find them in {0}'.format(bot.get_channel(624591866817413139).mention)
    await ctx.channel.send(msg)

#--- Channel help ----------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='channels', help='Displays you a summary of all channels and what they do')
async def on_command(ctx):
    await ctx.send(embed=channel_help())

#--- Resolve ---------------------------------------------------------------------------------------------------------------------------------------------------
def resolveEmoji():
    try:
        return discord.utils.get(bot.get_guild(479297254528647188).emojis, name='resolve');
    except:
        return ':resolve:'

def create_download_markdown(downloads):
    if downloads == None:
        return 'Not Available'
    string = ''
    if 'windows' in downloads:
        string += f"\n[Windows]({downloads['windows']})"
    if 'mac' in downloads:
        string += f"\n[MacOS]({downloads['mac']})"
    if 'linux' in downloads:
        string += f"\n[Linux]({downloads['linux']})"
    if string == '':
        return 'Not Available'
    else:
        return string[1:]


async def send_resolve_version_embed(ctx, release):
    embed = discord.Embed(title="DaVinci Resolve " + release['version'], description=release['shortDescription'], color=0xff8000, url=release['readMoreURL'])
    embed.set_footer(text="The staff does not take any responsibility for the above links.")
    embed.add_field(name="Resolve Free", value=create_download_markdown(release['downloads']['free']))
    embed.add_field(name="Resolve Studio", value=create_download_markdown(release['downloads']['studio']))
    embed.add_field(name=f'Recent Versions:', value='** / **'.join(allVisibleResolveVersionNames()))
    await ctx.send(embed=embed)
async def send_fusion_version_embed(ctx, release):
    embed = discord.Embed(title="Blackmagic Fusion " + release['version'], description=release['shortDescription'], color=0xff8000, url=release['readMoreURL'])
    embed.set_footer(text="The staff does not take any responsibility for the above links.")
    embed.add_field(name="Fusion Free", value=create_download_markdown(release['downloads']['free']))
    embed.add_field(name="Fusion Studio", value=create_download_markdown(release['downloads']['studio']))
    embed.add_field(name=f'Recent Versions:', value='** / **'.join(allVisibleFusionVersionNames()))
    await ctx.send(embed=embed)

@bot.command(name='resolve', help='Gives your the Download Link for the specified DaVinci Resolve Version. Leave empty to get the newest non-beta Release. Enter _!bmd resolve list_ to get a list of all available versions')
async def on_command(ctx, version=None, flag=None):
    if version == None:
        msg = str(resolveEmoji()) + 'No version provided, so here\'s the latest version of resolve.'
        await ctx.channel.send(msg)
        await send_resolve_version_embed(ctx, getResolveLatestData())
        return

    data = getResolveVersionData(version)
    if data != None:
        await send_resolve_version_embed(ctx, data)
    elif version == 'list':
        if flag == '-a':
            msg = str(resolveEmoji()) + 'Listing ***ALL*** available versions of DaVinci Resolve.\n```'
            versionNames = allResolveVersionNames()
        else:
            msg = str(resolveEmoji()) + 'Listing recent versions of DaVinci Resolve.\n```'
            versionNames = allVisibleResolveVersionNames()
        col = -1
        for version in versionNames:
            col += 1
            if col == 5:
                col = 0
                msg += '\n'
            msg += version + '        '[len(version):]
        msg += "\n```"
        await ctx.channel.send(msg)
    else:
        msg = str(resolveEmoji()) + 'Uh oh, that version of DaVinci Resolve doesn\'t exist. Here\'s the latest one.'
        await ctx.channel.send(msg)
        await send_resolve_version_embed(ctx, getResolveLatestData())

#--- Fusion ----------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='fusion', help='Gives your the Download Link for the specified Fusion Version. Leave empty to get the newest non-beta Release. Enter _!bmd fusion list_ to get a list of all available versions')
async def on_command(ctx, version=None, flag=None):
    if version == None:
        msg = str(resolveEmoji()) + 'No version provided, so here\'s the latest version of resolve.'
        await ctx.channel.send(msg)
        await send_fusion_version_embed(ctx, getResolveLatestData())
        return

    data = getFusionVersionData(version)
    if data != None:
        await send_fusion_version_embed(ctx, data)
    elif version == 'list':
        if flag == '-a':
            msg = str(resolveEmoji()) + 'Listing ***ALL*** available versions of Fusion.\n```'
            versionNames = allFusionVersionNames()
        else:
            msg = str(resolveEmoji()) + 'Listing recent versions of Fusion.\n```'
            versionNames = allVisibleFusionVersionNames()
        col = -1
        for version in versionNames:
            col += 1
            if col == 5:
                col = 0
                msg += '\n'
            msg += version + '        '[len(version):]
        msg += "\n```"
        await ctx.channel.send(msg)
    else:
        msg = str(resolveEmoji()) + 'Uh oh, that version of Fusion doesn\'t exist. Here\'s the latest one.'
        await ctx.channel.send(msg)
        await send_fusion_version_embed(ctx, getResolveLatestData())

#--- Compliment ------------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='compliment', help='Gives the tagges person a compliment')
async def on_command(ctx, user: discord.Member):
    compliments = [
        "You're doing great!", "You're awesome!", "Great filmmaker!", "Nice to see you!", "Nice camera!","You're that “Nothing” when people ask me what I'm thinking about.", "You look great today.", "You're a smart cookie.", "I bet you make babies smile.", "You have impeccable manners.", "I like your style.", "You have the best laugh.", "I appreciate you.", "You're an awesome friend.", "You're a gift to those around you.", "You're a smart cookie.", "You are awesome!", "You have impeccable manners.", "I like your style.", "You have the best laugh.", "I appreciate you.", "You are the most perfect you there is.", "You are enough.", "You're strong.", "Your perspective is refreshing.", "I'm grateful to know you.", "You light up the room.", "You deserve a hug right now.", "You should be proud of yourself.", "You're more helpful than you realize.", "You have a great sense of humor.", "You've got an awesome sense of humor!", "You are really courageous.", "Your kindness is a balm to all who encounter it.", "You're all that and a super-size bag of chips.", "On a scale from 1 to 10, you're an 11.", "You are strong.", "You're even more beautiful on the inside than you are on the outside.", "You have the courage of your convictions.", "I'm inspired by you.", "You're like a ray of sunshine on a really dreary day.", "You are making a difference.", "Thank you for being there for me.", "You bring out the best in other people.", "Your ability to recall random factoids at just the right time is impressive.", "You're a great listener.", "How is it that you always look great, even in sweatpants?", "Everything would be better if more people were like you!", "I bet you sweat glitter.", "You were cool way before hipsters were cool.", "That color is perfect on you.", "Hanging out with you is always a blast.", "You always know -- and say -- exactly what I need to hear when I need to hear it.", "You help me feel more joy in life.", "You may dance like no one's watching, but everyone's watching because you're an amazing dancer!", "Being around you makes everything better!", "When you say", "I meant to do that"," I totally believe you.", "When you're not afraid to be yourself is when you're most incredible.", "Colors seem brighter when you're around.", "You're more fun than a ball pit filled with candy. (And seriously, what could be more fun than that?)","That thing you don't like about yourself is what makes you so interesting.", "You're wonderful.", "You have cute elbows. For reals!", "Jokes are funnier when you tell them.", "You're better than a triple-scoop ice cream cone. With sprinkles.", "When I'm down you always say something encouraging to help me feel better.", "You are really kind to people around you.", "You're one of a kind!", "You help me be the best version of myself.", "If you were a box of crayons, you'd be the giant name-brand one with the built-in sharpener.", "You should be thanked more often. So thank you!!", "Our community is better because you're in it.", "Someone is getting through something hard right now because you've got their back. ", "You have the best ideas.", "You always find something special in the most ordinary things.", "Everyone gets knocked down sometimes, but you always get back up and keep going.", "You're a candle in the darkness.", "You're a great example to others.", "Being around you is like being on a happy little vacation.", "You always know just what to say.", "You're always learning new things and trying to better yourself, which is awesome.", "If someone based an Internet meme on you, it would have impeccable grammar.", "You could survive a Zombie apocalypse.", "You're more fun than bubble wrap.", "When you make a mistake, you try to fix it.", "Who raised you? They deserve a medal for a job well done.", "You're great at figuring stuff out.", "Your voice is magnificent.", "The people you love are lucky to have you in their lives.", "You're like a breath of fresh air.", "You make my insides jump around in the best way.", "You're so thoughtful.", "Your creative potential seems limitless.", "Your name suits you to a T.", "Your quirks are so you -- and I love that.", "When you say you will do something, I trust you.", "Somehow you make time stop and fly at the same time.", "When you make up your mind about something, nothing stands in your way.", "You seem to really know who you are.", "Any team would be lucky to have you on it.", "In high school I bet you were voted most likely to keep being awesome.", "I bet you do the crossword puzzle in ink.", "Babies and small animals probably love you.", "If you were a scented candle they'd call it Perfectly Imperfect (and it would smell like summer).", "There's ordinary, and then there's you.", "You're someone's reason to smile.", "You're even better than a unicorn, because you're real.", "How do you keep being so funny and making everyone laugh?", "You have a good head on your shoulders.", "Has anyone ever told you that you have great posture?", "The way you treasure your loved ones is incredible.", "You're really something special.", "Thank you for being you."

    ]
    await ctx.send(random.choice(compliments) + " " + user.mention)

#--- Give CPU and RAM Monitoring -------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='stats', help='Gives you the Status of the bot and server')
async def on_command(ctx):
    #if ctx.message.author.guild_permissions.administrator:
    embed = discord.Embed(title="Blackmagic Bot Statistics", color=0xff8000)
    embed.add_field(name='System Usage:', value=f'CPU: {psutil.cpu_percent()} RAM: {psutil.virtual_memory()[2]}')
    embed.add_field(name='Codeshare:', value='https://github.com/timhaettich/bmd')
    embed.add_field(name='Version::', value='v1.0.0 This bot is still in Development.')
    embed.add_field(name='Member count:', value='{0}'.format(bot.get_guild(479297254528647188).member_count),inline="false")
    embed.add_field(name='Bot written by:', value='This bot was written by @TimothyLH, additional features were contributed by @dave. This bot is based on discord.py', inline="false")
    await ctx.send(embed=embed)

#--- One time stuff --------------------------------------------------------------------------------------------------------------------------------------------
@bot.command(name='role-msg')
async def on_command(ctx):
    message = ("🎬 You can assign yourself a role here 🎬\n"
                "This will help others to quickly identify your interest and knowledge.\n\n"
                "Your occupation:\n"
                "📢  Director\n"
                "💰  Producer\n"
                "🎥 Camera Department\n"
                "🖥️  Post Production\n"
                "✍️  Writer\n"
                "👨  Hobbyist\n\n"
                "Your gear:\n"
                "🖥️  Post Production Gear\n"
                "🎥  Camera Gear\n"
                "📡  Broadcasting\n\n"
                "*Those roles are not pingable. You will not receive any additional pings*")
    ctx.send(message)


#---------------------------------------------------------------------------------------------------------------------------------------------------------------
bot.run(TOKEN)
