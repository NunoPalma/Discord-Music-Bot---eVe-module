import discord
from discord import VoiceChannel as vc
from discord.ext.commands import Bot
import discord.ext.commands as commands
from music.music_player import Music
from music.song import Song


class music_commands(commands.Cog):
	def __init__(self, bot):
		self.music_player = None
		self.bot = bot

	@commands.command(name= 'q')
	async def queue(self, ctx):
		if not self.music_player or self.music_player.queue_is_empty():
			await ctx.send("The queue is currently empty. Feel free to add some cool jams!")
			return

		await ctx.send(embed=self.music_player.get_queue())


	@commands.command(name = 'p')
	async def play(self, ctx, *, args):
		try:
			voice_channel = self.get_voice_channel(ctx, ctx.message.author)
		except TypeError:
			await ctx.send(ctx.message.author.mention + 
						"You must be in a voice channel if you want to headbang bro")
			return

		if not await self.bot_connected(voice_channel):
			self.music_player = Music(ctx)

		data_source, data = await self.music_player.create_source(args)
		song = Song(data)
		data['file_path'] = data_source
		data['requester'] = ctx.message.author

		await self.music_player.add_to_queue(discord.FFmpegPCMAudio(data_source), data)


	"""
	Disconnects the VoiceClient.
	@param ctx Current context
	"""
	@commands.command(name = 'stop')
	async def stop(self, ctx):
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I\'m not playing any song at the moment', delete_after=10)

		try:
			await ctx.guild.voice_client.disconnect() #Implement this on Music class
			await self.music_player.stop_queue_loop()
			self.music_player = None
		except AttributeError:
			pass

	"""
	If the VoiceClient is playing audio, then the current song is skipped.
	@param ctx Current context
	"""
	@commands.command(name = 'skip')
	async def skip(self, ctx):
		vc = ctx.voice_client
		if not vc or not vc.is_connected or self.music_player.queue_is_empty():
			return await ctx.send('I\'m not playing any song at the moment', delete_after=10)

		await self.music_player.skip(ctx)


	"""
	If the VoiceClient is playing audio, then the audio is paused.
	@param ctx Current context
	"""
	@commands.command(name  = 'pause')
	async def pause(self, ctx):
		vc = ctx.voice_client
		if vc and vc.is_playing():
			vc.pause()


	"""
	If the VoiceClient is playing audio, but is paused then the audio is resumed.
	@param ctx Current context
	"""
	@commands.command(name = 'resume')
	async def resume(self, ctx):
		vc = ctx.voice_client
		if vc and vc.is_paused():
			vc.resume()


	"""
	If the VoiceClient is playing audio, a visual representation of the current song
	will be presented on the channel where the command was invoked.
	@param ctx Current context
	"""
	@commands.command(name = 'current')
	async def current(self, ctx):
		vc = ctx.voice_client
		if vc and vc.is_playing and not self.music_player.queue_is_empty():
			await ctx.send(embed=self.music_player.get_current_song())


	"""
	Prints the commands' usage.
	@param ctx Current context
	"""
	@commands.command(name = 'help')
	async def current(self, ctx):
		embed = discord.Embed(color = discord.Colour.orange())

		embed.set_author(name='help')

		embed.add_field(name='?q', value='Queue information.', inline=False)
		embed.add_field(name='?current', value='Current music information.', inline=False)
		embed.add_field(name='?p', value='Plays the requested music.', inline=False)
		embed.add_field(name='?stop', value='Removes the bot from the voice channel. Queue is deleted.', inline=False)
		embed.add_field(name='?skip', value='Skips the current song.', inline=False)
		embed.add_field(name='?pause', value='Pauses the current song.', inline=False)
		embed.add_field(name='?resume', value='Resumes the previously paused song.', inline=False)

		await ctx.send(embed=embed)		


	"""
	Checks if a bot is connected to a certain voice channel. 
	If it isn't, then an attempt at connecting will be made

	@param voice_channel VoiceChannel we're trying to connect to
	@return a boolean value	-	True if the bot is already connected
							-	False if it isn't connected
	"""
	async def bot_connected(self, voice_channel):
		try:
			await voice_channel.connect(reconnect = True)
			return False
		except discord.ClientException:
			return True


	"""
	@param ctx Current context
	@param user The Member that sent the message
	@return VoiceChannel, if the user is at a Voice Channel
	@throws TypeError if the user isn't at a Voice Channel
	"""
	def get_voice_channel(self, ctx, user):
		for channel in self.bot.get_all_channels():
			if channel.type is discord.ChannelType.voice and user in channel.members:
				return channel
		raise TypeError


def setup(bot):
	bot.remove_command('help')
	bot.remove_command('current')
	bot.add_cog(music_commands(bot))
