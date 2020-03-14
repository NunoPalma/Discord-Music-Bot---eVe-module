import discord
import time

class Song():
	
	"""
	@param data a dictionary containing relevant information 
				to create a visual representation of the song
	"""
	def __init__(self, data):
		self.data = data


	"""
	This method will be used for a visual representation of the queue
	@param song_queue List of Songs
	@param data List of additional information
	@return Embed to be displayed
	"""
	def create_embed(self, song_queue=None, data=None):

		embed = (discord.Embed(title='Now playing',
							color=discord.Color.blurple())
				.add_field(name="Title", value=self.data['title'])
				.add_field(name="Requested by", value=self.data['requester'])
				.add_field(name='Duration', value=time.strftime('%M:%S', time.gmtime(self.data['duration'])))
				.set_thumbnail(url=self.data['thumbnail']))
		
		if not song_queue or len(song_queue) == 1:
			return embed

		embed.add_field(name='__**Up next**__', value= '\a' )

		i = 1
		total_songs_time = 0
		for song in song_queue[1:]:
			song_duration = song.data['duration']
			embed.add_field(name=str(i), value=song.data['title'] + ' | `'
											+ time.strftime('%M:%S', time.gmtime(song_duration))
											+ ' | Requested by: ' + str(song.data['requester'])
											+ '`', inline=False)
			i += 1
			total_songs_time += song_duration

		embed.add_field(name='Total time', value=time.strftime('%M:%S', time.gmtime(total_songs_time)))
		embed.add_field(name='Songs in queue', value=data['amount_songs'])

		return embed