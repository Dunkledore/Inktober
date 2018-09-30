import discord
from discord.ext import commands
import asyncio
import datetime
from config import token
bot = commands.Bot(command_prefix="?")

async def do_inktober():
	t = datetime.datetime.now()
	future = datetime.datetime(t.year, t.month, t.day+1, 0, 0)
	await asyncio.sleep((future-t).seconds)
	channel = bot.get_channel(495268727013507072)

	candidates = []
	async for message in channel.history(limit=5000, after=t):
		if message.attachments:
			if message.attachments[0].height:
				candidates.append(message)

	candidates_votes = {}
	for message in candidates:
		votes = 0
		for reaction in message.reactions:
			if reaction.emoji == "⬇":
				votes -= 1
			if reaction.emoji == "⬆":
				votes += 1
		candidates_votes[message] = votes

	ordered = []
	for message in sorted(candidates_votes, key=candidates_votes.get, reverse=True):
		ordered.append({message: candidates_votes[message]})

	embed = discord.Embed(title="Inktober", description=f"This winner of today's Inktober is {list(ordered[0].keys())[0].author.name}")
	await channel.send(embed=embed)
	bot.loop.create_task(do_inktober())



@bot.event
async def on_ready():
	print("on")
	bot.loop.create_task(do_inktober())


bot.run(token)




