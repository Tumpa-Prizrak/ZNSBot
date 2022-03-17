import disnake, json
from disnake.ext import commands

json_data = json.load(open("settings.json", "r"))

bot = commands.Bot(command_prefix=json_data["prefix"], case_insensitive=False, strip_after_prefix=True, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print("Ready!")

@bot.slash_command(name="ping", description="Shows ping of the bot.", guild_ids=[g.id for g in bot.guilds])
async def ping(interaction):
    await interaction.send(f"Pong in {round(bot.latency * 1000)} ms!")

@bot.slash_command(name="idea", description="Send an idea for bot")
async def idea(interaction):
    class MyModal(disnake.ui.Modal):
        def __init__(selfi) -> None:
            super().__init__(title="Идея",
                custom_id="idea_modal",
                components=[
                    disnake.ui.TextInput(
                        label="Текст предложения",
                        placeholder="Введите свою идею (макс. 1024 символа)",
                        custom_id="idea_content",
                        style=disnake.TextInputStyle.paragraph,
                        min_length=5,
                        max_length=1024,
                    ),
                ]
            )
        async def callback(selfi, interaction:disnake.ModalInteraction) -> None:
            await interaction.response.send_message(embed=disnake.Embed(title="Спасибо за Вашу идею!", description=interaction.text_values["idea_content"]))
            await bot.get_channel(954016631430991942).send(embed=disnake.Embed(title=f"Идея от {interaction.author} ({interaction.author.id})", description=interaction.text_values["idea_content"]))

        async def on_error(selfi, error, inter) -> None:
            await inter.response.send_message("Упс... Что-то пошло не так...", ephemeral=True)

    await interaction.response.send_modal(MyModal())


bot.run(json_data["token"])