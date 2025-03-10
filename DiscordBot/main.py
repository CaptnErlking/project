import discord
from discord.ext import commands
import asyncio
import re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
iv_logs = {}
hunt_mode = "H"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

hunt_pokemon_set = {
    "ditto", "arctozolt", "arctovish", "dracovish",
    "charmander", "bulbasaur", "squirtle",
    "chikorita", "cyndaquil", "totodile",
    "torchic", "treecko", "mudkip",
    "chimchar", "turtwig", "piplup",
    "snivy", "tepig", "oshawott",
    "chespin", "fennekin", "froakie",
    "rowlet", "litten", "popplio",
    "grookey", "sobble", "scorbunny"
}


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "shiny":
        await message.channel.send("You'll get it 😉")
        shiny_trigger_active = True
        return

    if message.author.bot:
        print(f"Message from bot: {message.author}")
        print("Message Content:", message.content)

        if message.embeds:
            for i, embed in enumerate(message.embeds, start=1):
                print(f"\nEmbed {i}:")

                if embed.title:
                    print("Title:", embed.title)

                if embed.description:
                    print("Description:", embed.description)

                    if "wild" in embed.description.lower() and "★" in embed.description:
                        await lock_channel_for_10_seconds(message.channel)
                        return

                    if hunt_mode == "H":
                        embed_lower = embed.description.lower()
                        for pokemon in hunt_pokemon_set:
                            if "wild" in embed_lower and f"{pokemon}" in embed_lower and "appeared" in embed_lower:
                                await message.channel.send(
                                    f"Ayo!!\nIt's a starter Encounter!!\nCheck Balls\nDon't Forget to check the weather Conditions before catching this BadBoi!!"
                                )
                                return

                    elif "wild" in embed.description.lower() and "greninja-ash" in embed.description.lower() and "appeared" in embed.description.lower():
                        await message.channel.send("Finally!!\nIt's A Greninja-Ash Encounter!!\nCheck Balls\nDon't Forget to check the weather Conditions before catching this BadBoi!!")
                        await lock_channel_for_10_seconds(message.channel)
                        return


                if embed.author:
                    print("Author:", embed.author.name if embed.author.name else "No author name")
                    pokemon_name = embed.author.name.split(' ')[0]
                    await calculate_iv_percentage(embed, message.channel, pokemon_name)

                if embed.footer:
                    print("Footer:", embed.footer.text if embed.footer.text else "No footer text")
                    if "Opponent's" in embed.footer.text:
                        await send_private_message_to_user("captn_erlking", "An embed message has 'Opponent's' in the footer.")
                        await send_private_message_to_user("tapadum", "An embed message has 'Opponent's' in the footer.")

    await bot.process_commands(message)

async def lock_channel_for_10_seconds(channel):
    try:
        overwrite = channel.overwrites_for(channel.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
        await channel.send("@everyone 🔒 Channel locked for 10 seconds due to a wild Crazy Pokémon encounter!")
        await asyncio.sleep(10)
        overwrite.send_messages = None
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrite)
        await channel.send("🔓 Channel unlocked!")
    except discord.Forbidden:
        await channel.send("❌ I don't have permission to lock this channel.")

async def send_private_message_to_user(username, message_content):
    for guild in bot.guilds:
        member = discord.utils.find(lambda m: m.name == username, guild.members)
        if member:
            try:
                await member.send(message_content)
                print(f"Sent private message to {username}")
            except discord.Forbidden:
                print(f"Could not send private message to {username}")
            break
    else:
        print(f"User {username} not found in any guilds.")


async def calculate_iv_percentage(embed, channel, pokemon_name):
    iv_field = next((field.value for field in embed.fields if field.name == "IVs"), None)

    if iv_field:
        iv_match = re.search(r'HP: (\d+), Atk: (\d+), Def: (\d+), SpA: (\d+), SpD: (\d+), Spe: (\d+)', iv_field)

        if iv_match:
            ivs = list(map(int, iv_match.groups()))
            total_iv = sum(ivs)
            max_iv = 31 * 6
            iv_percentage = (total_iv / max_iv) * 100
            iv_logs[pokemon_name] = iv_percentage
            await channel.send(f"The IV of {pokemon_name} is {iv_percentage:.2f}% and has been logged.")

@bot.command(name="huntmode")
async def hunt_mode_command(ctx):
    global hunt_mode

    message = await ctx.send(
        "Choose your hunt mode:\n:regional_indicator_s: Shiny Hunt (Ditto, Arctozolt, Arctovish, and Dracovish messages will not show up)\n:regional_indicator_h: Pokemon Hunt (All messages will show up)"
    )

    await message.add_reaction("\U0001f1f8")  # :regional_indicator_s:
    await message.add_reaction("\U0001f1ed")  # :regional_indicator_h:

    def check(reaction, user):
        return (
            user != bot.user
            and str(reaction.emoji) in ["\U0001f1f8", "\U0001f1ed"]
            and reaction.message.id == message.id
        )

    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

        if str(reaction.emoji) == "\U0001f1f8":  # :regional_indicator_s:
            hunt_mode = "S"
            await message.edit(content="Hunt mode set to Shiny Hunt. Messages for Ditto, Arctozolt, Arctovish, and Dracovish will not show up.")

        elif str(reaction.emoji) == "\U0001f1ed":  # :regional_indicator_h:
            hunt_mode = "H"
            await message.edit(content="Hunt mode set to Pokemon Hunt. All messages will show up.")

    except asyncio.TimeoutError:
        await message.edit(content="No reaction received. Hunt mode remains unchanged.")

    finally:
        await message.clear_reactions()


@bot.command(name="ivlogs")
async def display_iv_logs(ctx):
    if iv_logs:
        logs = "\n".join([f"{name}: {iv:.2f}%" for name, iv in iv_logs.items()])
        await ctx.send(f"**IV Logs:**\n{logs}")
    else:
        await ctx.send("No IV logs available.")

@bot.command(name="remove_pokemon")
async def remove_pokemon(ctx, pokemon_name: str):
    if pokemon_name in iv_logs:
        del iv_logs[pokemon_name]
        await ctx.send(f"{pokemon_name} has been removed from the IV logs.")
    else:
        await ctx.send(f"{pokemon_name} not found in the IV logs.")

@bot.command(name="clear_ivlogs")
async def clear_iv_logs(ctx):
    iv_logs.clear()
    await ctx.send("All IV logs have been cleared.")

bot.run('-')
