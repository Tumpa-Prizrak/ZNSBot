import nextcord
import asyncio, random, anekos, aiohttp
from nextcord.ext import commands, tasks
from urllib.parse import quote
class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # блэклист категорий будет позже, а пока будете смотреть на футанари и трапов :)
    @nextcord.slash_command(name="nekos", description="Получает картинку из Nekos (18+ допустимо только в NSFW-каналах)")
    async def nekos_(self, interaction: nextcord.Interaction, category: str = nextcord.SlashOption(name = "category", description = "Категория картинки", required=False)):
        if category is not None:
            if category not in anekos.possible:
                await interaction.send(f"Категории `{category}` не существует! Я отправлю список тебе в ЛС")
                await interaction.user.send(embed = nextcord.Embed(title = "Категории Nekos", description = ", ".join(anekos.everywhere)+(", "+", ".join(anekos.nsfw) if interaction.channel.is_nsfw() else "")))
                return
            if category in anekos.nsfw and not interaction.channel.is_nsfw():
                return await interaction.send("Вы не можете воспользоваться командой с NSFW-категорией вне NSFW-канала")
        else:
            category = random.choice(anekos.nsfw if interaction.channel.is_nsfw() else anekos.everywhere)
        img = await anekos.img(category)
        await interaction.send(embed = nextcord.Embed(title = f'Nekos {category.capitalize()}', url = img).set_image(url = img))

    @nextcord.slash_command(name = "rule34", description = "Получает картинку из Rule34 (только в NSFW-каналах)")
    async def rule34(self, interaction: nextcord.Interaction, tag: str = nextcord.SlashOption(name='tag', description = "Тег, по которому нужно найти картинку", required = True)):
        if not interaction.channel.is_nsfw(): return await interaction.send("Вы не можете воспользоваться командой вне NSFW-канала")
        apibase = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit=20&tags={}&json=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(apibase.format(quote(tag))) as response:
                if (await response.text()) == '':
                    return await interaction.send('По данному тегу ничего не нашлось :(')
                r = random.choice((await response.json()))
        # response = requests.get(apibase.format(tag))
        # if response.text == '': return await interaction.send('По данному тегу ничего не нашлось :(')
        # r = random.choice(response.json()) # TODO: ujson.loads
        await interaction.send(embed = nextcord.Embed(title = 'rule34.xxx', url = r.get('file_url')).set_footer(text=f"Теги: {self.bot.minify_text(r.get('tags', 'нет'))}").set_image(url = r.get('file_url')))

def setup(bot):
    bot.add_cog(NSFW(bot))
    print('Ког "NSFW" загружен')
def teardown(bot):
    print('Ког "NSFW" отгружен')