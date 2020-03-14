import asyncio
import music
from async_timeout import timeout
import os
from music.song import Song
from music.YTDLsource import YTDLsource


class Music():
	def __init__(self, ctx):
		self.ctx = ctx
		self.bot = ctx.bot
		self.guild = ctx.guild
		self.queue = asyncio.Queue()
		self.songs = []
		self.next = asyncio.Event()
		self.current_song = None
		self.DOWNLOAD_DIRECTORY = 'music/downloads/'
		self.ytsource = YTDLsource()

		self.task = self.bot.loop.create_task(self.queue_loop())


	async def create_source(self, args):
		return await self.ytsource.create_source(args)


	def get_queue(self):
		queue = []

		for song in self.songs:
			queue.append(Song(song))

		data = {'amount_songs': self.queue.qsize()}
		return queue[0].create_embed(song_queue=queue, data=data)


	def queue_is_empty(self):
		return False if self.current_song else True


	async def add_to_queue(self, song, data):
		await self.queue.put(song)
		self.songs.append(data)


	def pop_queue_element(self):
		self.queue.get()


	def remove_download_file(self, file_path):
		if os.path.exists(file_path):
			os.remove(file_path)
		else:
			print("The file doesn't exist") #Might be better to just handle the exception here


	def cleanup(self):
		for file in os.listdir(self.DOWNLOAD_DIRECTORY):
			file_path = self.DOWNLOAD_DIRECTORY + file
			os.remove(file_path)


	async def stop_queue_loop(self):
		self.task.cancel
		self.cleanup()


	def get_current_song(self):
		song = Song(self.current_song[1])
		return song.create_embed()


	async def queue_loop(self):

		await self.bot.wait_until_ready()

		while not self.bot.is_closed():
			self.next.clear()

			try:
				async with timeout(300):
					source = await self.queue.get()
					data = self.songs[0]
			except asyncio.TimeoutError:
				await self.ctx.voice_client.disconnect()
				await self.stop_queue_loop()
				return

			self.current_song = [source, data]

			self.guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

			await self.next.wait()
			self.remove_download_file(data['file_path'])

			source.cleanup()
			self.current_song = None
			self.songs.pop(0)

