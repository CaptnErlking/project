import discord
from discord.ext import commands
import asyncio
import re

intents = discord.Intents.default()
intents.message_content = True  # Ensure Message Content Intent is enabled

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if "Vs.​ ​ ​​★" is in the message content
    if "Vs.​ ​ ​​★" in message.content:
        await lock_channel_for_10_seconds(message.channel)
        return

    # Check each embed for the "Vs.​ ​ ​​★" text
    for embed in message.embeds:
        if embed.description and "Vs.​ ​ ​​★" in embed.description:
            await lock_channel_for_10_seconds(message.channel)
            return

        # Check embeds for the IV data
        await calculate_iv_percentage(embed, message.channel)

async def lock_channel_for_10_seconds(channel):
    try:
        # Create a permission overwrite to prevent sending messages
        overwrite = channel.overwrites_for(channel.guild.default_role)
        overwrite.send_messages = False

        await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
        await channel.send("@everyone 🔒 Channel locked for 10 seconds due to shiny Pokémon encounter!")

        await asyncio.sleep(10)  # Wait 10 seconds

        # Reset permissions to default (allow sending messages)
        overwrite.send_messages = None
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
        await channel.send("🔓 Channel unlocked!")

    except discord.Forbidden:
        await channel.send("❌ I don't have permission to lock this channel.")

async def calculate_iv_percentage(embed, channel):
    # Extract the field with the name "IVs"
    iv_field = next((field.value for field in embed.fields if field.name == "IVs"), None)
    
    if iv_field:
        # Regex to match IV values in the format: "HP: 27, Atk: 29, Def: 19, SpA: 29, SpD: 9, Spe: 31"
        iv_match = re.search(r'HP: (\d+), Atk: (\d+), Def: (\d+), SpA: (\d+), SpD: (\d+), Spe: (\d+)', iv_field)
        
        if iv_match:
            # Extract the IV values from the regex groups and convert them to integers
            ivs = list(map(int, iv_match.groups()))
            
            # Calculate IV percentage
            total_iv = sum(ivs)
            max_iv = 31 * 6
            iv_percentage = (total_iv / max_iv) * 100
            
            # Send the result
            await channel.send(f"The IV of this Pokémon is {iv_percentage:.2f}%")
        else:
            await channel.send("❌ Couldn't calculate IVs. Please make sure the IVs are in the correct format.")

bot.run('MTMwMDQ2MTY1MTI0OTg1NjU5Mg.Gb1hwM.jfhD0vGUbTke9o_bOhitXLzdyohRaf9V0dQI9k')
