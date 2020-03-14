from youtube_dl import YoutubeDL
from functools import partial
import asyncio


class YTDLsource():
	def __init__(self):
		ytdlopts = {
    		'format': 'bestaudio/best',
    		'outtmpl': 'music/downloads/%(title)s',
    		'restrictfilenames': True,
    		'noplaylist': True,
    		'nocheckcertificate': True,
   			'ignoreerrors': False,
    		'logtostderr': False,
    		'quiet': True,
    		'no_warnings': True,
    		'default_search': 'auto',
    		'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
		}

		self.ytdl = YoutubeDL(ytdlopts)


	def assemble_data(self, data):
		new_data = {}
		new_data['thumbnail'] = data['thumbnail']
		new_data['duration'] = data['duration']
		new_data['title'] = data['title']

		return new_data


	async def create_source(self, url):
		to_run = partial(self.ytdl.extract_info, url=url)
		data = await asyncio.get_event_loop().run_in_executor(None, to_run)
		
		if 'entries' in data:
			data = self.assemble_data(data['entries'][0])

		return [self.ytdl.prepare_filename(data), data]