import nextcord
import asyncio
from nextcord.ext import commands, tasks
class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="avatar", description = 'Показывает аватар пользователя')
    async def avatar(self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(name = "user", description = "Пользователь, чей аватар надо показать", required = False)):
        member = member if member else interaction.user
        emb = nextcord.Embed(title = f'Автар пользователя {member}:', color = member.accent_color or 0x000000)
        emb.set_image(url = member.avatar.url if member.avatar else member.default_avatar)
        await interaction.send(embed = emb)


def setup(bot):
    bot.add_cog(Other(bot))
    print('Ког "Other" загружен')
def teardown(bot):
    print('Ког "Other" отгружен')