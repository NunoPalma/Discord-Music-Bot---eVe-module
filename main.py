from discord.ext.commands import Bot
from discord.ext.commands import errors
from discord import ClientException
import config


def instantiate_bot():
	bot = Bot(command_prefix = '?')

	for file in config.BOT_COGS:
		try:
			bot.load_extension(file)
		except errors.ExtensionNotFound:
			print(f'Failed to find the extension {file}.')

	try:
		print('Bot is running.')
		bot.run(config.SECRET_KEY)
	except (KeyboardInterrupt, ClientException) as e:
		print('Bot is shutting down.')
		exit(1)


if __name__ == "__main__":
	instantiate_bot()