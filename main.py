import keep_alive
import discord
import os
import random
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
start_time = datetime.utcnow()


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
    print(f'{bot.user.name} has connected to Discord server {guild.name}(id: {guild.id})  {start_time}\n')
    await bot.change_presence(activity=discord.Game("кости | !help - F.A.Q."))


@bot.event
async def on_member_update(before, after):  # send in text channel information about members status changes
    for guild in bot.guilds:
        category = guild.categories[0]
        channel = category.channels[4]
    if str(before.status) == "online" or "offline":
        status_msg = "{} has gone {}!".format(after.name, after.status)
        await channel.send(status_msg)


@bot.command(name='help', pass_context=True)
@commands.has_permissions(administrator=True)
async def help_command(ctx):  # give list of bot commands
    command_prefix = '!'
    emb = discord.Embed(title=' F.A.Q.:clipboard: ')
    emb.description = "Список команд бота"
    emb.add_field(name='{}clear :broom: '.format(command_prefix), value='Очистка чата (Админ)')
    emb.add_field(name='{}d6 :game_die: '.format(command_prefix), value='Roll D6')
    emb.add_field(name='{}d20 :game_die: '.format(command_prefix), value='Roll D20')
    emb.add_field(name='{}uptime :timer: '.format(command_prefix), value='Аптайм бота')
    emb.add_field(name='{}donate :moneybag: '.format(command_prefix), value='Поддержать проект')
    await ctx.send(embed=emb)


@bot.command(name='clear', pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):  # clear chat
    await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, укажите аргумент (количество удаляемых сообщений)!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, не достаточно прав для выполнения данной команды!')


@bot.command(name="uptime", pass_context=True)
async def up_cmd(ctx):  # show bot uptime
    now = datetime.utcnow()
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    fmt = "{h}h {m}m {s}s"
    if days:
        fmt = "{d}d " + fmt
    fmt = fmt.format(fmt, d=days, h=hours, m=minutes, s=seconds)
    await ctx.send(fmt)


@bot.command(name='donate', pass_context=True)
async def donate(ctx):  # give link to Donate
    donation_alerts = 'Вот ссылочка на DonationAlerts:\nhttps://www.donationalerts.com/r/mineneet'
    embed_obj = discord.Embed(description=donation_alerts)
    await ctx.send(embed=embed_obj)
    await ctx.send(file=discord.File('donate.png'))


@bot.command(name='d6', pass_context=True)
async def d6_roll(ctx):  # roll d6 dice
    d6_list = ['d6/dice1.png',
               'd6/dice2.png',
               'd6/dice3.png',
               'd6/dice4.png',
               'd6/dice5.png',
               'd6/dice6.png']
    roll_d6 = random.choice(d6_list)
    await ctx.send(file=discord.File(roll_d6))


@bot.command(name='d20', pass_context=True)
async def d20_roll(ctx):  # roll d20 dice
    d20_list = ['d20/dice1.png', 'd20/dice6.png', 'd20/dice11.png', 'd20/dice16.png',
                'd20/dice2.png', 'd20/dice7.png', 'd20/dice12.png', 'd20/dice17.png',
                'd20/dice3.png', 'd20/dice8.png', 'd20/dice13.png', 'd20/dice18.png',
                'd20/dice4.png', 'd20/dice9.png', 'd20/dice14.png', 'd20/dice19.png',
                'd20/dice5.png', 'd20/dice10.png', 'd20/dice15.png', 'd20/dice20.png']
    roll_d20 = random.choice(d20_list)
    await ctx.send(file=discord.File(roll_d20))


keep_alive.keep_alive()
bot.run(TOKEN)