import discord
from discord import VoiceChannel as vc
from discord.ext.commands import Bot
import discord.ext.commands as commands

class poll_commands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.poll_list = {}
		self.poll_description = ""

	@commands.command(name= 'poll')
	async def poll(self, ctx, *, args):
		self.poll_description = args

		suggestions = args.split("#")

		for i in range(1, len(suggestions)):
			value = self.trim_string(suggestions[i])

			self.poll_list[value] = 0
			await ctx.send("Adding " + value + " to the poll!")

	@commands.command(name= 'vote')
	async def vote(self, ctx, *, args):
		value = args.split("#")[1]
		value = self.trim_string(value)
		if value not in self.poll_list.keys():
			await ctx.send(value + " isn't in the poll list yet. Feel free to add it.")
			return

		poll_list[value] += 1

		
	@commands.command(name= 'end')
	async def end(self, ctx):
		result = max(self.poll_list, key=self.poll_list.get)

		poll_list = {}

		await ctx.send("The winner is " + result + " with " + poll_list[result] + " votes.")

	def trim_string(self, value):
		if value[len(value) - 1] == " ":
			value = value[:-1]

		return value	

def setup(bot):
	bot.add_cog(poll_commands(bot))	