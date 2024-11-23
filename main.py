import json
import discord
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.all())

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config.get("TOKEN")

@bot.event
async def on_ready():
    print(f"\nWe have logged in as: {bot.user.display_name}")

@bot.event
async def on_application_command_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            description=f"<a:denied:1309555101609889843> {error}",
            color=discord.Color.red()
        )
        await ctx.respond(embed=embed)
    else:
        raise error
    
@bot.slash_command(name='send_tos')
async def send_tos(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Terms of Service",
        description="By using this service, you accept the [Discord ToS](https://discord.com/terms), and the following terms",
        color=discord.Color.green()
    )

    embed.add_field(
        name="User Liability",
        value="While using this service, it is your duty to ensure that you are reading and acknowledging provided prompts. User errors are not insured, and will result in the loss of your cryptocurrency/valuables.",
        inline=False
    )

    embed.add_field(
        name="Service Safety",
        value="If we perceive something as suspicious, or against the ToS, we have the authority to decline your request. Any deals involving gift cards, accounts, or unfamiliar content is prohibited.",
        inline=False
    )

    embed.add_field(
        name="Account Security",
        value="While using this service, it is your responsibility to ensure the safety of your account. If your account is compromised, we are not liable for any losses.",
        inline=False
    )

    embed.add_field(
        name="User Guarantee",
        value="By using this service, you are guaranteed the safety of your funds. All funds lost in our possession following a bot error will be compensated 1:1. User errors will not be compensated.",
        inline=False
    )

    embed.set_footer(text="Bob MM", icon_url=bot.user.avatar.url)  
    await ctx.respond(embed=embed)
    

"""
cogs = [
    'cogs.tickets',
    'cogs.other',
    'cogs.self_roles',
    'cogs.fun',
    'cogs.verify',
    'cogs.mod',
    'cogs.utility',
]

for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)
"""

bot.run(TOKEN)