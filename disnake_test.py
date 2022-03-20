import disnake, json
from disnake.ext import commands, tasks
import os, sys, asyncio, aiohttp, time, datetime, random, requests, platform, pyautogui, aeval


json_data = json.load(open("settings.json", "r"))

bot = commands.Bot(command_prefix=json_data["prefix"], case_insensitive=False, strip_after_prefix=True, intents=disnake.Intents.all())

async def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content
minify_text = lambda txt: f'{str(txt)[:900]}...\n...и ещё {len(str(txt).replace(str(txt)[900:], ""))} символов...' if len(str(txt)) >= 1024 else str(txt)
super_minify_text = lambda txt: f'{str(txt)[:132]}...\n...и ещё {len(str(txt).replace(str(txt)[132:], ""))} символов...' if len(str(txt)) >= 256 else str(txt)
creators = [555638466365489172, 529302484901036043]

@bot.event
async def on_ready():
    print("Ready!")

@bot.slash_command(name="ping", description="Shows ping of the bot.", guild_ids=[g.id for g in bot.guilds])
async def ping(interaction):
    await interaction.send(f"Pong in {round(bot.latency * 1000)} ms!")

@bot.slash_command(name="idea", description="Send an idea for bot")
async def idea(interaction, idea: str = commands.Param(
    name = 'Idea', description ="Text of your idea"
)):
    # class MyModal(disnake.ui.Modal):
    #     def __init__(selfi) -> None:
    #         super().__init__(title="Идея",
    #             custom_id="idea_modal",
    #             components=[
    #                 disnake.ui.TextInput(
    #                     label="Текст предложения",
    #                     placeholder="Введите свою идею (макс. 1024 символа)",
    #                     custom_id="idea_content",
    #                     style=disnake.TextInputStyle.paragraph,
    #                     min_length=5,
    #                     max_length=1024,
    #                 ),
    #             ]
    #         )
    #     async def callback(selfi, interaction:disnake.ModalInteraction) -> None:
    #         await interaction.response.send_message(embed=disnake.Embed(title="Спасибо за Вашу идею!", description=interaction.text_values["idea_content"]))
    #         msg = await bot.get_channel(954016631430991942).send(embed=disnake.Embed(title=f"Идея от {interaction.author} ({interaction.author.id})", description=interaction.text_values["idea_content"]))
    #         await msg.create_thread(name = "Обсуждение")
    #         await msg.add_reaction("👍")
    #         await msg.add_reaction("👎")

    #     async def on_error(selfi, error, inter) -> None:
    #         await inter.response.send_message("Упс... Что-то пошло не так...", ephemeral=True)

    # await interaction.response.send_modal(MyModal())
    await interaction.response.send_message(embed=disnake.Embed(title="Спасибо за Вашу идею!", description=idea))
    msg = await bot.get_channel(954016631430991942).send(embed=disnake.Embed(title=f"Идея от {interaction.author} ({interaction.author.id})", description=idea))
    await msg.create_thread(name = "Обсуждение")
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

# мне пиздец лень переписывать под слеши
@bot.command()
async def logout(ctx, timerout: int = None):
    if ctx.author.id in creators:
        if timerout is None:
            await ctx.send('Отключаюсь')
            print('Отключение...')
            await bot.close()
            print('Отключено')
        else:
            await ctx.send(f'Отключение от Discord через {timerout} секунд')
            await asyncio.sleep(timerout)
            print('Отключение...')
            await bot.close()
            print('Отключено')
    else:
        await ctx.send("Нет! Тебе нельзя меня выключить!")
@bot.command()
async def restart(ctx, timerout: int = None):
    if ctx.author.id in creators:
        if timerout is None:
            await ctx.send('Перезапуск!')
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await ctx.send(f'Отключение от Discord через {timerout} секунд')
            await asyncio.sleep(timerout)
            await ctx.send('Перезапуск!')
            os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await ctx.send("Нет! Тебе нельзя меня перезагрузить!")
@bot.command(aliases = ['eval', 'aeval', 'evaulate', 'выполнить', 'exec', 'execute'])
async def __eval(ctx, *, arg):
    if ctx.author.id not in creators: return await ctx.send("Кыш!")
    code = await clean_code(arg)
    standart_args = {
        "disnake": disnake,
        "discord": disnake,
        "commands": commands,
        "bot": bot,
        "tasks": tasks,
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
        # 'logger': bot.logger
    }
    start = time.time()
    try:
        bot.logger.info(f'Invoked command "eval"')
        r = await aeval.aeval(f"""{code}""", standart_args, {})#aioconsole.aexec(f"""{code}""", standart_args)
        ended = time.time() - start
        print(r)
        if not code.startswith('#nooutput'):
            await ctx.send(embed = disnake.Embed(title = "Успешно!", description = f"Выполнено за: {ended}", color = 0x99ff99).add_field(name = f'Входные данные:', value = f'`{minify_text(code)}`').add_field(name = f'Выходные данные:', value = f'`{minify_text(r)}`', inline=False))
        bot.logger.success(f'Command "eval" executed in {ended}')
    except Exception as e:
        ended = time.time() - start
        # await ctx.send(embed = discord.Embed(title = f"При выполнении возникла ошибка. Время: {ended}", description = f'Ошибка:\n```py\n{"".join(format_exception(e, e, e.__traceback__))}```', color = 0xff000))
        if not code.startswith('#nooutput'):
            await ctx.send(embed = disnake.Embed(title = f"При выполнении возникла ошибка.\nВремя: {ended}", description = f'Ошибка:\n```py\n{e}```', color = 0xff0000).add_field(name = f'Входные данные:', value = f'`{minify_text(code)}`', inline=False))
        bot.logger.error(f'Command "eval" execution failed in {ended}:\n\t\tPython error: {e}')
        raise e

bot.run(json_data["token"])