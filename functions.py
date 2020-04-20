"""
Blackmagic Design Discord Community bot: functions file
Version 1.0.0
Written by TimothyLH

ChangeLog:
v1.0.0
Introduces a basic set of functions
"""
#Imports
import discord

class HelpFunctions:
    #Constructor
    def __init__(self,bot):
        self.bot = bot

    #Function to generate channel help embed
    def channel_help(self):
        embed = discord.Embed(title="Channel Overview", description="See what each channel is for below:", color=0xff8000)
        embed.set_footer(text="Contact Staff for more informations")
        for ch in this.bot.get_guild(guild).channels:
            embed.add_field(ch.name, value=ch.topic)
        return embed


    #Function to get emojis
    def emoji(self,name):
        return discord.utils.get(this.bot.get_guild(guild).emojis, name=name)
