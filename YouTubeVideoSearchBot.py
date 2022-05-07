from youtube_search import YoutubeSearch
import config

from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import hashlib, os

print(1)
URL_APP = 'https://188.225.77.119:443'

def searcher(text):
	res = YoutubeSearch(text, max_results=10).to_dict()
	return res
print(11)
bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
print(2)
async def on_startup(dp):
	print(3)
	await bot.set_webhook(URL_APP)
	print(4)

async def on_shutdown(dp):
	await bot.delete_webhook()

@dp.inline_handler()
async def start(message: types.Message):
	await message.answer('Напиши: @YouTubeVideoSearchBot и название видео')

@dp.inline_handler()
async def inline_handler(query : types.InlineQuery):
	text = query.query or 'echo'
	links = searcher(text)

	articles = [types.InlineQueryResultArticle(
		id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
		title = f'{link["title"]}',
		url = f'https://www.youtube.com/watch?v={link["id"]}',
		thumb_url = f'{link["thumbnails"][0]}',
		input_message_content=types.InputTextMessageContent(
			message_text=f'https://www.youtube.com/watch?v={link["id"]}')
	) for link in links]

	await query.answer(articles, cache_time=60, is_personal=True)

executor.start_webhook(
	dispatcher=dp,
	webhook_path='',
	on_startup=on_startup,
	on_shutdown=on_shutdown,
	skip_updates=True,
	host="127.0.0.1",
	port=3003
	)