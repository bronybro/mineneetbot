import keep_alive
import discord
import os
import datetime
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
client = discord.Client()
now = datetime.datetime.now()


@bot.command(name='donate', pass_context=True)
async def donate(ctx):  # give link to Donate
    donation_alerts = 'Вот ссылочка на DonationAlerts:\nhttps://www.donationalerts.com/r/mineneet'
    embed_obj = discord.Embed(description=donation_alerts)
    await ctx.send(embed=embed_obj)
    await ctx.send(file=discord.File('donate.png'))


@bot.event
async def on_member_join(member):  # say "Hello" when someone join GUILD
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}! Добро пожаловать на наш ламповый сервер!')


@bot.event
async def on_ready():  # set bot ptesence
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user.name} has connected to Discord {now.strftime("%d-%m-%Y %H:%M")}\n'
          f'{guild.name}(id: {guild.id})\n')
    await bot.change_presence(activity=discord.Game("кости"))


@bot.event
async def on_member_update(before, after):  # send in rexr channel information about membes status changes
    for guild in bot.guilds:
        category = guild.categories[0]
        channel = category.channels[1]
    if str(before.status) == "online" or "offline":
        status_msg = "{} has gone {}!".format(after.name, after.status)
        await channel.send(status_msg)


@bot.command(name='d6', pass_context=True)
async def d6(ctx):  # roll d6 dice
    d6_list = ['d6/dice1.png',
               'd6/dice2.png',
               'd6/dice3.png',
               'd6/dice4.png',
               'd6/dice5.png',
               'd6/dice6.png']
    roll_d6 = random.choice(d6_list)
    await ctx.send(file=discord.File(roll_d6))


@bot.command(name='d20', pass_context=True)
async def d20(ctx):  # roll d20 dice
    d20_list = ['d20/dice1.png', 'd20/dice6.png', 'd20/dice11.png', 'd20/dice16.png',
                'd20/dice2.png', 'd20/dice7.png', 'd20/dice12.png', 'd20/dice17.png',
                'd20/dice3.png', 'd20/dice8.png', 'd20/dice13.png', 'd20/dice18.png',
                'd20/dice4.png', 'd20/dice9.png', 'd20/dice14.png', 'd20/dice19.png',
                'd20/dice5.png', 'd20/dice10.png', 'd20/dice15.png', 'd20/dice20.png']
    roll_d20 = random.choice(d20_list)
    await ctx.send(file=discord.File(roll_d20))


keep_alive.keep_alive()
bot.run(TOKEN)
