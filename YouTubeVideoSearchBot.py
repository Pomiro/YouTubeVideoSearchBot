from youtube_search import YoutubeSearch
import config

from aiogram import Bot, types, utils
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import hashlib, os

def searcher(text):
	res = YoutubeSearch(text, max_results=10).to_dict()
	return res

bot = Bot(token = config.TOKEN)
dp = Dispatcher(bot)

WEBHOOK_HOST = 'pomiro.space'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_BASE = "https://{}:{}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(config.TOKEN)

async def on_startup(dp):
	await bot.set_webhook(config.URL_APP)

async def on_shutdown(dp):
	await bot.delete_webhook()

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



# executor.start_polling(dp, skip_updates=True)

executor.start_webhook(
	dispatcher=dp,
	webhook_path='',
	on_startup=on_startup,
	on_shutdown=on_shutdown,
	skip_updates=True,
	host="0.0.0.0",
	port=3001
	)