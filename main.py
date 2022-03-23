import re
import nextcord, json, aeval, asyncio, aiohttp, os, sys, time, datetime, random, requests, pyautogui, platform, blusutils
from nextcord.ext import commands


json_data = json.load(open("settings.json", "r"))
bot = commands.Bot(command_prefix=json_data["prefix"], case_sensitive=True, strip_after_prefix=True, intents=nextcord.Intents.all())

minify_text = lambda txt: f'{str(txt)[:900]}...\n...и ещё {len(str(txt).replace(str(txt)[900:], ""))} символов...' if len(str(txt)) >= 1024 else str(txt)
bot.minify_text = minify_text
super_minify_text = lambda txt: f'{str(txt)[:132]}...\n...и ещё {len(str(txt).replace(str(txt)[132:], ""))} символов...' if len(str(txt)) >= 256 else str(txt)
bot.super_minify_text = super_minify_text
async def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content
bot.clean_code = clean_code


@bot.event
async def on_ready():
    print("Ready!")

@bot.listen("on_message") # listen как event, но их можно делать сколько угодно
async def reps(message: nextcord.Message):
    if message.content.lower().startswith(("+rep", "-rep")):
        marr = message.content.split(" ")
        action = marr[0][:1] # когда будет бд, будем менять репу
        whoreps = await message.guild.get_member(int(marr[1][2:-1])) if re.match(r"<@\d+>", marr[1])\
            else (await message.channel.fetch_message(message.reference.message_id)).author if message.reference\
                else await message.reply(f'Я не могу понять, кому нужно {"добавить" if action == "+" else "убрать"} репутацию!')\
                    and blusutils.anywhere_raise(commands.errors.BadArgument(f"Invalid argument for {marr[0]}: {marr[1]}")) # вот он и пригодился). люблю тернарники
        await message.reply(f'{marr[0].upper()} {whoreps.mention}: {" ".join(marr[2:])}')


@bot.slash_command(name="ping", description="Показывает пинг бота.", guild_ids=[g.id for g in bot.guilds])
async def ping(interaction: nextcord.Interaction):
    await interaction.send(f"Pong in {round(bot.latency * 1000)} ms!")

@bot.slash_command(name="idea", description="Отправляет идею для бота.")
async def idea(interaction: nextcord.Interaction, idea_text: str = nextcord.SlashOption(name="text", description="Ваша идея")):
    try:
        msg = await bot.get_channel(json_data["idea_channel"]).send(embed=nextcord.Embed(title=f"Идея от {interaction.user} ({interaction.user.id})", description=idea_text))
        await msg.create_thread(name = "Обсуждение")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        await interaction.response.send_message(embed=nextcord.Embed(title="Спасибо за Вашу идею!", description="Текст вашей идеи: " + idea_text))
    except Exception as e:
        await interaction.response.send_message(embed=nextcord.Embed(title="Произошла неожиданная ошибка", description="Ошибка: " + str(e)))
        raise e




# Модалки надо бы...
# @bot.user_command(name='Пожаловаться', description = 'Пожаловаться на пользователя')
# async def complaint_user_command(interaction: nextcord.Interaction):
#     pass

@bot.command(aliases = ['eval', 'aeval', 'evaulate', 'выполнить', 'exec', 'execute'])
async def __eval(ctx, *, arg):
    if ctx.author.id not in json_data["creators"]: return await ctx.send("Кыш!")
    code = await clean_code(arg)
    standart_args = {
        "nextcord": nextcord,
        "discord": nextcord,
        "commands": commands,
        "bot": bot,
        "ctx": ctx,
        "asyncio": asyncio,
        "aiohttp": aiohttp,
        "os": os,
        'sys': sys,
        "time": time,
        "datetime": datetime,
        "random": random,
        "requests": requests,
        "pyautogui": pyautogui,
        'platform': platform,
        'blusutils': blusutils
    }
    start = time.time()
    try:
        r = await aeval.aeval(f"""{code}""", standart_args, {})#aioconsole.aexec(f"""{code}""", standart_args)
        ended = time.time() - start
        print(r)
        if not code.startswith('#nooutput'):
            await ctx.send(embed = nextcord.Embed(title = "Успешно!", description = f"Выполнено за: {ended}", color = 0x99ff99).add_field(name = f'Входные данные:', value = f'`{minify_text(code)}`').add_field(name = f'Выходные данные:', value = f'`{minify_text(r)}`', inline=False))
    except Exception as e:
        ended = time.time() - start
        # await ctx.send(embed = discord.Embed(title = f"При выполнении возникла ошибка. Время: {ended}", description = f'Ошибка:\n```py\n{"".join(format_exception(e, e, e.__traceback__))}```', color = 0xff000))
        if not code.startswith('#nooutput'):
            await ctx.send(embed = nextcord.Embed(title = f"При выполнении возникла ошибка.\nВремя: {ended}", description = f'Ошибка:\n```py\n{e}```', color = 0xff0000).add_field(name = f'Входные данные:', value = f'`{minify_text(code)}`', inline=False))
        raise e

@bot.command(aliases = ['cl', 'load', 'l', 'cogload'])
async def cog_load(ctx, *, cogname):
    if ctx.author.id in json_data['creators']:
        async def loading(cog_now):
            try:
                bot.load_extension(f'cogs.{cog_now[:-3].replace(" ", "_")}')
                return f'Ког {cog_now[:-3]} успешно загружен'
            except commands.ExtensionAlreadyLoaded:
                return f'Ког {cog_now[:-3]} уже загружен!'
            except commands.NoEntryPointError:
                return f'Ког {cog_now[:-3]} не имеет входной точки (функции setup), пропуск'
            except commands.errors.ExtensionNotFound:
                return f'Ког {cogname} не обнаружен'
            except Exception as excepted:
                await ctx.send(f'Ошибка кога {cog_now[:-3]}:```py\n{excepted}```\nПодробнее в консоли')
                raise excepted
        if cogname == 'all':
            await ctx.send("\n".join([await loading(now_cog) for now_cog in os.listdir("./cogs") if now_cog.endswith(".py")]))
        else:
            await ctx.send((await loading(cogname+'.py')))
@bot.command(aliases = ['cul', 'unload', 'ul', 'cogunload'])
async def cog_unload(ctx, *, cogname):
    if ctx.author.id in json_data['creators']:
        async def unloading(cog_now):
            try:
                bot.unload_extension(f'cogs.{cog_now[:-3].replace(" ", "_")}')
                return f'Ког {cog_now[:-3]} успешно отгружен'
            except commands.ExtensionNotLoaded:
                return f'Ког {cog_now[:-3]} уже отгружен!'
            except commands.NoEntryPointError:
                return f'Ког {cog_now[:-3]} не имеет входной точки (функции setup), пропуск'
            except commands.errors.ExtensionNotFound:
                return f'Ког {cogname} не обнаружен'
            except Exception as excepted:
                await ctx.send(f'Ошибка кога {cog_now[:-3]}:```py\n{excepted}```\nПодробнее в консоли')
                raise excepted
        if cogname == 'all':
            await ctx.send("\n".join([await unloading(now_cog) for now_cog in os.listdir("./cogs") if now_cog.endswith(".py")]))
        else:
            await ctx.send((await unloading(cogname+'.py')))
@bot.command(aliases = ['crl', 'reload', 'rl', 'cogreload'])
async def cog_reload(ctx, *, cogname):
    if ctx.author.id in json_data['creators']:
        async def reloading(cog_now):
            try:
                bot.unload_extension(f'cogs.{cog_now[:-3].replace(" ", "_")}')
                bot.load_extension(f'cogs.{cog_now[:-3].replace(" ", "_")}')
            except commands.errors.ExtensionNotLoaded:
                bot.load_extension(f'cogs.{cog_now[:-3].replace(" ", "_")}')
            except commands.errors.ExtensionNotFound:
                return f'Ког {cogname} не обнаружен'
            except commands.NoEntryPointError:
                return f'Ког {cog_now[:-3]} не имеет входной точки (функции setup), пропуск'
            except Exception as excepted:
                await ctx.send(f'Ошибка:```py\n{excepted}```\nПодробнее в консоли')
                raise excepted
            return f'Ког {cog_now[:-3]} успешно перезгружен'
        if cogname == 'all':
            await ctx.send("\n".join([await reloading(now_cog) for now_cog in os.listdir("./cogs") if now_cog.endswith(".py")]))
        else:
            await reloading(cogname+'.py')

for i in os.listdir("./cogs"):
    if i.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{i[:-3].replace(' ', '_')}")
        except (commands.errors.ExtensionNotFound, commands.NoEntryPointError):
            print(f'invalid ext {i}')

bot.run(json_data["token"])