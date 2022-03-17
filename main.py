import nextcord, json
from nextcord.ext import commands

json_data = json.load(open("settings.json", "r"))

bot = commands.Bot(command_prefix=json_data["prefix"], case_sensitive=True, strip_after_prefix=True, intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    print("Ready!")

@bot.command()
async def ping():
    print(f"Pong in {round(bot.latency * 1000)} ms!")

bot.run(json_data["token"])