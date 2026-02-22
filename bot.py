import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

# ------- CONFIG -------
SS_CHANNEL_ID = 1473050690359398460      # ← YOUR SS CHANNEL ID
ROLE_ID = 1377211761496948797            # ← ROLE GIVEN AFTER SUBSCRIBE
YT_LINK = "https://youtube.com/@saraikiplays-s"  # Your YouTube Link
# -----------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ----------------------------------------------------------
#  EVENT: Bot Ready
# ----------------------------------------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash Commands Synced: {len(synced)}")
    except Exception as e:
        print(e)

# Bot Activity 
  
    stream = discord.Streaming(
        name="@SARAIKI PLAYS-S",
        url=YT_LINK,  # Yeh link zaroor dena hota hai
        platform="You Tube"  # Optional
    )

    await bot.change_presence(status=discord.Status.dnd, activity=stream)

# ----------------------------------------------------------
#  MESSAGE LISTENER FOR SS CHANNEL
# ----------------------------------------------------------
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # If message is in screenshot channel
    if message.channel.id == SS_CHANNEL_ID:

        # ALLOW ONLY IMAGES
        if len(message.attachments) == 0:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} ⚠ **Only YouTube Channel Subscribe Image Allowed!**",
                delete_after=5
            )
            return

        # GIVE ROLE FOR SUBSCRIBE
        guild = message.guild
        role = guild.get_role(ROLE_ID)

        if role in message.author.roles:
            await message.channel.send(
                f"{message.author.mention} ✔ You already have **{role.name}** role!",
                delete_after=6
            )
            return

        # Give Role
        await message.author.add_roles(role)

        # Send Beautiful Thank You Message
        embed = discord.Embed(
            title="😘 Thanks For Subscribing!",
            description=f"{message.author.mention}\nYou received {role.mention}.\n**Love You Ho Gaya Mari Jaan**\n\n**Apni Profile Check Kr Loo!**",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=message.author.avatar.url)
        embed.set_footer(text="@Saraiki Plays-s")
      
        await message.channel.send(embed=embed)

    await bot.process_commands(message)


# ----------------------------------------------------------
#  SLASH COMMAND: /notify
# ----------------------------------------------------------
@bot.tree.command(name="notify", description="Send Subscribe Notification")
async def notify(interaction: discord.Interaction):

    embed = discord.Embed(
        title="AoA Mari Piary Public 😘",
        description="Yara Subscribe My Channel\nAnd Get **Special Role** in Server.",
        color=discord.Color.red()
    )

    embed.add_field(name="Channel:", value=YT_LINK, inline=False)
    embed.set_footer(text="@Saraiki Plays-s")
    embed.set_thumbnail(url=interaction.guild.icon.url)

    button = discord.ui.Button(
        label="Subscribe Now",
        url=YT_LINK,
        style=discord.ButtonStyle.link
    )

    view = discord.ui.View()
    view.add_item(button)

    await interaction.response.send_message(embed=embed, view=view)


bot.run(TOKEN)
