import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = discord.Client(intents=intents)

RULES_MESSAGE_ID = 0  # We'll update this soon
MEMBER_ROLE_ID = 0    # We'll update this soon
EMOJI = "✅"

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == RULES_MESSAGE_ID and str(payload.emoji) == EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(MEMBER_ROLE_ID)
        member = payload.member
        if role and member and not member.bot:
            await member.add_roles(role)

@bot.event 
async def on_raw_reaction_remove(payload):
    if payload.message_id == RULES_MESSAGE_ID and str(payload.emoji) == EMOJI:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(MEMBER_ROLE_ID)
        member = await guild.fetch_member(payload.user_id)
        if role and member:
            await member.remove_roles(role)

bot.run(os.environ['TOKEN'])
