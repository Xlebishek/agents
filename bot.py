import asyncio
import logging
import api_bot

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from agents import agents_dict
from router import router_agent  # роутер

BOT_TOKEN = api_bot.api_bot

logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

now_agent = 'router_agent'

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Здравствуй, я бот-помощник по учёбе, твой вопрос?")

# нужна нормальная логика ветвления, LangGraph?
@dp.message()
async def handle_message(message: types.Message):
    global now_agent

    user_query = message.text
    user_name = message.from_user.username

    if now_agent == 'router_agent':
        now_agent = router_agent(user_query) # вызов

    current_agent = agents_dict.get(now_agent)

    if current_agent is None:
        await message.answer("Извините, я не отвечаю на подобного рода вопросы, может помочь чем-то ещё?")
        return

    answer = current_agent(user_query, user_name) # вызов

    if answer == 'error':
        now_agent = 'router_agent'
        await message.answer("Извините, я не отвечаю на подобного рода вопросы, может помочь чем-то ещё?")
        return

    await message.answer(answer)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
