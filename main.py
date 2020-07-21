import discord
from discord.ext import commands, tasks
import datetime
from ruamel.yaml import YAML
from itertools import cycle
import random
import os

yaml = YAML()

with open("./Config.yml", "r", encoding = "utf-8") as file:
    config = yaml.load(file)




bot = commands.Bot(command_prefix=config['Prefix'], description="Joshy's_bot", case_insensitive=True)

logs_channel_id = config['Log Channel ID']
# status = cycle(bot.status)

bot.embed_color = discord.Color.from_rgb(
config['Embed Settings']['Color']['r'],
config['Embed Settings']['Color']['g'],
config['Embed Settings']['Color']['b']
)
bot.footer = config['Embed Settings']['Footer']['Text']
bot.footer_image = config['Embed Settings']['Footer']['Icon URL']
bot.prefix = config['Prefix']
bot.TOKEN = os.getenv(config['Bot Token Variable Name'])
bot.responses = config['Responses']
bot.status = config['Status']

# bot.playing_status = config['Playing Status'].format(prefix = bot.prefix)

status = cycle(bot.status)

extensions = sorted([
    'Cogs.general'
])

for extension in extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} and connected to discord! (ID: {bot.user.id})")

    # game = discord.Game(name = bot.playing_status)
    # await bot.change_presence(activity = game)
    change_status.start()

    embed = discord.Embed(
        title = f"{bot.user.name} Online!",
        color = bot.embed_color,
        timestamp = datetime.datetime.now(datetime.timezone.utc)
    )
    embed.set_footer(
        text = bot.footer,
        icon_url = bot.footer_image
    )

    bot.channel = bot.get_channel(logs_channel_id)
    await bot.channel.send(embed = embed)


@bot.command(name = "restart", aliases = ["r"], help = "Restarts the bots")
@commands.has_permissions(ban_members=True)
async def restart(ctx):
    embed = discord.Embed(
    title = f"{bot.user.name} Restarting!",
    color = bot.embed_color,
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    )

    embed.set_author(
    name = ctx.author.name,
    icon_url = ctx.author.avatar_url
    )

    embed.set_footer(
        text = bot.footer,
        icon_url = bot.footer_image
    )

    await bot.channel.send(embed = embed)

    await ctx.message.add_reaction('✅')
    await bot.close()

# __________________________________________________________________________________________________
@bot.event
async def on_member_join(member):
    print(f'{member} has joined a server')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')


@bot.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):

    embed = discord.Embed(
        title = f"Question: {question}\n",
        color = bot.embed_color,
    )
    embed.set_footer(
    text = f"Answer: {random.choice(bot.responses)}",
        icon_url = bot.footer_image
    )

    bot.channel = bot.get_channel(logs_channel_id)
    await bot.channel.send(embed = embed)

    # await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount = 10):
    await ctx.channel.purge(limit=amount + 1)


@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)


@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(bot.TOKEN, bot=True, reconnect=True)
