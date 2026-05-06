import discord
from discord.ext import commands
import os

# Enable all intents needed
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

# Get secrets from Replit
TOKEN = os.environ['TOKEN']
RULES_MESSAGE_ID = int(os.environ['RULES_MESSAGE_ID'])
MEMBER_ROLE_ID = int(os.environ['MEMBER_ROLE_ID'])

@client.event
async def on_ready():
    print(f'Bot logged in as {client.user}')
    print('Bot is ready!')

@client.event
async def on_raw_reaction_add(payload):
    # Ignore bot's own reactions
    if payload.user_id == client.user.id:
        return
    
    # Check if reaction is on rules message
    if payload.message_id == RULES_MESSAGE_ID and str(payload.emoji) == "✅":
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(MEMBER_ROLE_ID)
        
        if role and member:
            try:
                await member.add_roles(role)
                await member.send("Welcome to **JIMZ EXPLOITS**! You now have access to the server.")
                
                # Remove reaction so they can re-react if needed
                channel = client.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, member)
            except Exception as e:
                print(f"Error giving role: {e}")

@client.command()
async def setuprules(ctx):
    """Posts the rules embed with JIMZ EXPLOITS title"""
    await ctx.message.delete()  # Delete the !setuprules message
    
    embed = discord.Embed(
        title="JIMZ EXPLOITS",
        description="**RULES:**",
        color=0x00ff00  # Green
    )
    
    embed.add_field(name="1. ⛔ Spamming", value="Spamming, flooding or sending unnecessary messages is strictly prohibited.", inline=False)
    embed.add_field(name="2. 🤝 Be respectful", value="Be respectful to everyone. Insults, harassment and toxic behavior are not allowed.", inline=False)
    embed.add_field(name="3. 📢 Advertising", value="Advertising or sharing links to other servers is prohibited.", inline=False)
    embed.add_field(name="4. 🔞 NSFW", value="Sharing 18+ content, explicit images or links is strictly forbidden.", inline=False)
    embed.add_field(name="5. 💻 Scripts", value="Using shared scripts for malicious or harmful purposes is prohibited.", inline=False)
    embed.add_field(name="6. 🛑 Selling", value="Selling, re-uploading or claiming ownership of scripts without permission is not allowed.", inline=False)
    embed.add_field(name="7. 🎭 Impersonating", value="Impersonating staff members or other users is strictly prohibited.", inline=False)
    embed.add_field(name="8. ⚠️ Punishment", value="Violating server rules will result in a mute or permanent ban.", inline=False)
    
    embed.add_field(name="⚠️ DISCLAIMER", value="This server is for educational purposes only.\nAll scripts shared here are intended solely for learning and development.\nWe do not encourage or support any malicious use.", inline=False)
    
    embed.set_footer(text="React with ✅ to agree to the rules")
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    
    await ctx.send(f"✅ Rules posted! New Message ID: `{msg.id}`\nUpdate your RULES_MESSAGE_ID secret with this.", delete_after=20)

@client.command()
async def ping(ctx):
    """Check if bot is alive"""
    await ctx.send("Pong! 🏓 I'm online")

client.run(TOKEN)
