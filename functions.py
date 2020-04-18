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

#Function to generate channel help embed
def channel_help():
    embed = discord.Embed(title="Channel Overview", description="See what each channel is for below:", color=0xff8000)
    embed.set_footer(text="Contact Staff for more informations")
    embed.add_field(name="#💡-rules-and-info", value=f"Overview of the rules in this server and a quick introduction to it.")
    embed.add_field(name="#📢-announcements", value=f"Announcements about things related to this Discord Server and Blackmagic")
    embed.add_field(name="#💕-partners", value=f"We are partnered with other great Servers, that are worth it to check out too!")
    embed.add_field(name="#🕴🏻-roles", value=f"Assign yourself an occupation and equipment you use, so everyone directly knows what you are up to.")
    embed.add_field(name="#🎨-resolve", value=f"For all questions about Resolve, including Color Grading.")
    embed.add_field(name="#💥-fusion", value=f"For all questions about Fusion and VFX.")
    embed.add_field(name="#🎧-fairlight", value=f"For all questions about Audio in Fairlight.")
    embed.add_field(name="#🔌-equipment", value=f"For all questions about Blackmagic Products.")
    embed.add_field(name="#💬-hangout", value=f"Have a chat with other fellow filmmakers, please keep it kids friendly and without spam.")
    embed.add_field(name="#📐-your-work", value=f"Made something cool? Share it with us!")
    embed.add_field(name="#📸-your-gear", value=f"Built a cool camera rig, editing suite? Share it here.")
    embed.add_field(name="#🌈-color-me", value=f"Would you like to know how others would color grade your image? Share it in here in a high quality format.")
    embed.add_field(name="#💻-terminal", value=f"Want to check your rank? Play another song? Send the command in here!")
    return embed
