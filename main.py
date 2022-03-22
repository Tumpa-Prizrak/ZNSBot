import nextcord, json, aeval, asyncio, aiohttp, os, sys, time, datetime, random, requests, pyautogui, platform, anekos, blusutils, nekos
from nextcord.ext import commands

json_data = json.load(open("settings.json", "r"))
bot = commands.Bot(command_prefix=json_data["prefix"], case_sensitive=True, strip_after_prefix=True, intents=nextcord.Intents.all())

minify_text = lambda txt: f'{str(txt)[:900]}...\n...и ещё {len(str(txt).replace(str(txt)[900:], ""))} символов...' if len(str(txt)) >= 1024 else str(txt)
super_minify_text = lambda txt: f'{str(txt)[:132]}...\n...и ещё {len(str(txt).replace(str(txt)[132:], ""))} символов...' if len(str(txt)) >= 256 else str(txt)
async def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

@bot.event
async def on_ready():
    print("Ready!")

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


# блэклист категорий будет позже, а пока будете смотреть на футанари и трапов :)
@bot.slash_command(name="nekos", description="Получает картинку из Nekos (18+ допустимо только в NSFW-каналах)")
async def nekos_(interaction: nextcord.Interaction, category: str = nextcord.SlashOption(name = "text", description = "Категория картинки", required=False)):
    if category is not None:
        if category not in anekos.possible:
            await interaction.send(f"Категории `{category}` не существует! Я отправлю список тебе в ЛС")
            await interaction.user.send(embed = nextcord.Embed(title = "Категории Nekos", description = ", ".join(anekos.everywhere)+(", "+", ".join(anekos.nsfw) if interaction.channel.is_nsfw() else "")))
        if category in anekos.nsfw and not interaction.channel.is_nsfw():
            return await interaction.send("Вы не можете воспользоваться командой с NSFW-категорией вне NSFW-канала")
    else:
        category = random.choice(anekos.nsfw if interaction.channel.is_nsfw() else anekos.everywhere)
    img = nekos.img(category)
    await interaction.send(embed = nextcord.Embed(title = f'Nekos {category.capitalize()}', url = img).set_image(url = img))

            

# @bot.command(aliases = ['eval', 'aeval', 'evaulate', 'выполнить', 'exec', 'execute'])
# async def __eval(ctx, *, arg):
#     if ctx.author.id not in json_data["creators"]: return await ctx.send("Кыш!")
#     code = await clean_code(arg)
#     standart_args = {
#         "nextcord": nextcord,
#         "discord": nextcord,
#         "commands": commands,
#         "bot": bot,
#         "ctx": ctx,
#         "asyncio": asyncio,
#         "aiohttp": aiohttp,
#         "os": os,
#         'sys': sys,
#         "time": time,
#         "datetime": datetime,
#         "random": random,
#         "requests": requests,
#         "pyautogui": pyautogui,
#         'platform': platform
#     }
#     start = time.time()
#     try:
#         r = await aeval.aeval(f"""{code}""", standart_args, {})#aioconsole.aexec(f"""{code}""", standart_args)
#         ended = time.time() - start
#         print(r)
#         if not code.startswith('#nooutput'):
#             await ctx.send(embed = nextcord.Embed(title = "Успешно!", description = f"Выполнено за: {ended}", color = 0x99ff99).add_field(name = f'Входные данные:', value = f'`{minify_text(code)}`').add_field(name = f'Выходные данные:', value = f'`{minify_text(r)}`', inline=False))
#     except Exception as e:
#         ended = time.time() - start
#         # await ctx.send(embed = discord.Embed(title = f"При выполнении возникла ошибка. Время: {ended}", description = f'Ошибка:\n```py\n{"".join(format_exception(e, e, e.__traceback__))}```', color = 0xff000))
#         if not code.startswith('#nooutput'):
#             await ctx.send(embed = nextcord.Embed(title = f"При выполнении возникла ошибка.\nВремя: {ended}", description = f'Ошибка:\n```py\n{e}```', color = 0xff0000).add_field(name = f'Входные данные:', value = f'`{minify_text(code)}`', inline=False))
#         raise e

bot.run(json_data["token"])