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
# @commands.has_permissions(administrator=True)
async def send_tos(ctx: discord.ApplicationContext):
    embed_tos = discord.Embed(
        title="Terms of Service",
        description="__By using this service, you accept the [Discord ToS](https://discord.com/terms), and the following terms__",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed_tos)

    embed_liability = discord.Embed(
        title="User Liability",
        description="While using this service, it is your duty to ensure that you are reading and acknowledging provided prompts. User errors are not insured, and will result in the loss of your cryptocurrency/valuables.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed_liability)

    embed_safety = discord.Embed(
        title="Service Safety",
        description="If we perceive something as suspicious, or against the ToS, we have the authority to decline your request. Any deals involving gift cards, accounts, or unfamiliar content is prohibited.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed_safety)

    embed_security = discord.Embed(
        title="Account Security",
        description="While using this service, it is your responsibility to ensure the safety of your account. If your account is compromised, we are not liable for any losses.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed_security)

    embed_guarantee = discord.Embed(
        title="User Guarantee",
        description="By using this service, you are guaranteed the safety of your funds. All funds lost in our possession following a bot error will be compensated 1:1. User errors will not be compensated.",
        color=discord.Color.green()
    )
    embed_guarantee.set_footer(text="Halal MM", icon_url=bot.user.avatar.url)
    await ctx.send(embed=embed_guarantee)

    
@bot.slash_command(name='send_crypto')
#@commands.has_permissions(administrator=True)
async def send_crypto(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Cryptocurrency",
        color=discord.Color.green()
    )
    embed.add_field(
        name="__**Fees:**__",
        value=(
            "Deals $250+: 1%\n"
            "Deals under $250: $2\n"
            "__Deals under $50 are **FREE**__\n\n"
            "Press the dropdown below to select & initiate a deal involving either **Bitcoin**, **Ethereum**, **Litecoin**, or **Solana**."
        ),
        inline=False
    )

    # Define the dropdown menu
    class CryptoDropdown(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(label="Bitcoin", emoji="<:1425bitcoin:1309555011105062985>"),
                discord.SelectOption(label="Ethereum", emoji="<:3031ethereum:1309555027618037781>"),
                discord.SelectOption(label="Litecoin", emoji="<:4887ltc:1309555034534576150>"),
                discord.SelectOption(label="Solana", emoji="<:solanasol:1309885313744633866>"),
            ]
            super().__init__(placeholder="Make a selection", options=options)

        async def callback(self, interaction: discord.Interaction):
            # Create a ticket channel
            category = interaction.guild.get_channel(1309552867748610068)
            if not category or not isinstance(category, discord.CategoryChannel):
                await interaction.response.send_message("Category not found or invalid!", ephemeral=True)
                return

            channel_name = f"ticket-{interaction.user.name}".lower()
            ticket_channel = await category.create_text_channel(
                name=channel_name,
                topic=f"Crypto ticket for {self.values[0]}",
                reason=f"Ticket created by {interaction.user} for {self.values[0]}"
            )

            await ticket_channel.send(
                content=f"{interaction.user.mention}, your ticket has been created for **{self.values[0]}**.",
                embed=discord.Embed(
                    description=f"Support will assist you shortly.",
                    color=discord.Color.green()
                )
            )
            await interaction.response.send_message(
                f"Your ticket has been created: {ticket_channel.mention}", ephemeral=True
            )

    view = discord.ui.View()
    view.add_item(CryptoDropdown())

    await ctx.send(embed=embed, view=view)


@bot.slash_command(name='send_passes')
#@commands.has_permissions(administrator=True)
async def send_passes(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="Passes",
        color=discord.Color.green()
    )
    embed.add_field(
        name="__**Description:**__",
        value=(
            "Purchase Passes to speed up your tickets, and save money if you are a returning client. Passes are able to be used in tickets to expedite your deals by simply selecting the Pass option.\n\n"
            "To check your balance, use the `/passes` command. A pass accounts for $2, making deals $500+ deduct 1+ passes.\n\n"
            "**Bulk Pricing:**\n"
            "__10–20 passes:__ $1.75/per\n"
            "__20+ passes:__ $1.45/per"
        ),
        inline=False
    )

    # Dropdown menu setup
    select = discord.ui.Select(
        placeholder="Make a selection",
        options=[
            discord.SelectOption(label="Bitcoin", emoji="<:1425bitcoin:1309555011105062985>"),
            discord.SelectOption(label="Ethereum", emoji="<:3031ethereum:1309555027618037781>"),
            discord.SelectOption(label="Litecoin", emoji="<:4887ltc:1309555034534576150>"),
            discord.SelectOption(label="Solana", emoji="<:solanasol:1309885313744633866>"),
        ]
    )

    view = discord.ui.View()
    view.add_item(select)

    await ctx.send(embed=embed, view=view)


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