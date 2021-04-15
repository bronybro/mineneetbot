#!/usr/bin/python3.7
import os
import random
import discord
import nekos

from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from utils import default

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # bot token from .env
GUILD = os.getenv('DISCORD_GUILD')  # guild id from .env

config = default.config()

bot = commands.Bot(command_prefix=config["prefix"],prefix=config["prefix"])
bot.remove_command('help')

start_time = datetime.utcnow()


@bot.event
async def on_member_join(member):  # say "Hello" when someone join GUILD
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}! Добро пожаловать на наш ламповый сервер!')


@bot.event
async def on_ready():  # set bot presence
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user.name} has connected to Discord server {guild.name}(id: {guild.id})  {start_time}\n')
    await bot.change_presence(activity=discord.Game("кости | !help - F.A.Q."))


@bot.event
async def on_member_update(before, after):  # send in text channel information about members status changes
    for guild in bot.guilds:
        category = guild.categories[0]
        channel = category.channels[4]  # [4] - special channel to see users activities
    if str(before.status) == "online" or "offline":
        status_msg = "{} has gone {}!".format(after.name, after.status)
        await channel.send(status_msg)


@bot.command(name='help', pass_context=True)
@commands.has_permissions(administrator=True)
async def help_command(ctx):  # give list of bot commands
    command_prefix = '!'
    emb = discord.Embed(title=' F.A.Q.:clipboard: ', color=0x2ecc71)
    emb.description = "Список команд бота"
    emb.add_field(name='{}clear :broom: '.format(command_prefix), value='Очистка чата (Админ)')
    emb.add_field(name='{}mute :mute: '.format(command_prefix), value='Выдать мут чата (Админ)')
    emb.add_field(name='{}unmute :speaker: '.format(command_prefix), value='Снять мут чата (Админ)')
    emb.add_field(name='{}kick :wastebasket: '.format(command_prefix), value='Кикнуть пользователя (Админ)')
    emb.add_field(name='{}ban :banana: '.format(command_prefix), value='Забанить пользователя (Админ)')
    emb.add_field(name='{}d6 :game_die: '.format(command_prefix), value='Roll D6')
    emb.add_field(name='{}d20 :game_die: '.format(command_prefix), value='Roll D20')
    emb.add_field(name='{}uptime :timer: '.format(command_prefix), value='Аптайм бота')
    emb.add_field(name='{}pic :frame_photo: '.format(command_prefix), value='Получить картинку или gif')
    emb.add_field(name='{}hentai :heart_eyes: '.format(command_prefix), value='Получить 18+ картинку или gif(NSFW)')
    emb.add_field(name='{}donate :moneybag: '.format(command_prefix), value='Поддержать проект')
    await ctx.send(embed=emb)


@bot.command(name='clear', pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):  # clear chat
    await ctx.channel.purge(limit=amount + 1)


@bot.command(name='kick', pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):  # kick user from server
    emb = discord.Embed(title='Kick :wave:', colour=discord.Color.red())
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Kick user', value='Kicked user : {}'.format(member.mention))
    emb.set_footer(text='Был выгнан с сервера администратором {}'.format(ctx.author.name),
                   icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command(name='ban', pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):  # ban user
    emb = discord.Embed(title='Ban :lock:', colour=discord.Color.dark_red())

    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)

    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Ban user', value='Baned user : {}'.format(member.mention))
    emb.set_footer(text='Был заблокирован администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb)


@bot.command(name='mute', pass_context=True)
@commands.has_permissions(administrator=True)
async def mute_user(ctx, member: discord.Member):  # mute user
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Mute :mute:', colour=discord.Color.gold())
    mute_role = discord.utils.get(ctx.message.guild.roles, name='MUTED')
    await member.add_roles(mute_role)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='MUTE', value='Muted user : {}'.format(member.mention))
    emb.set_footer(text='Был помещён в мут администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@bot.command(name='unmute', pass_context=True)
@commands.has_permissions(administrator=True)
async def mute_user(ctx, member: discord.Member):  # unmute user
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Mute :speaker:', colour=discord.Color.gold())
    mute_role = discord.utils.get(ctx.message.guild.roles, name='MUTED')
    await member.remove_roles(mute_role)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='MUTE', value='Muted user : {}'.format(member.mention))
    emb.set_footer(text='Мут снят администратором {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, укажите аргумент (количество удаляемых сообщений)!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, не достаточно прав для выполнения данной команды!')


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')


@mute_user.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.name}, вы не обладаете такими правами!')


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
    donation_alerts = 'Вот ссылочка на DonationAlerts:\nhttps://www.donationalerts.com/'
    embed_obj = discord.Embed(description=donation_alerts)
    await ctx.send(embed=embed_obj)
    await ctx.send(file=discord.File('files/donate.png'))


@bot.command(name='d6', pass_context=True)
async def d6_roll(ctx):  # roll d6 dice
    dir = 'files/d6'
    roll_d6 = os.path.join(dir, random.choice(os.listdir(dir)))
    await ctx.send(file=discord.File(roll_d6))


@bot.command(name='d20', pass_context=True)
async def d20_roll(ctx):  # roll d20 dice
    dir = 'files/d20'
    roll_d20 = os.path.join(dir, random.choice(os.listdir(dir)))
    await ctx.send(file=discord.File(roll_d20))


def is_nsfw():
    async def predicate(ctx):
        return ctx.channel.is_nsfw()
    return commands.check(predicate)


@bot.command(name='hentai', pass_context=True)
@is_nsfw()
async def give_hentai(ctx, arg):

    if arg in config["hentai"]:
        emb = discord.Embed(color=0x2ecc71)
        emb.set_image(url=nekos.img(str(arg)))
        emb.description = "#" + arg
        await ctx.send(embed=emb)


@bot.command(name='pic', pass_context=True)
async def give_pic(ctx, arg):

    if arg in config["pic"]:
        emb = discord.Embed(color=0x2ecc71)
        emb.set_image(url=nekos.img(str(arg)))
        emb.description = "#" + arg
        await ctx.send(embed=emb)


bot.run(TOKEN)
