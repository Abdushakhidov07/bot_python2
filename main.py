from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv 
from service import *
from connection import *
import asyncio
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()



main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Мои задачи")],
        [KeyboardButton(text="🆘 Помощь")],
    ],
    resize_keyboard=True,
)








@dp.message(CommandStart())
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"Hello @{message.from_user.username}", reply_markup=main_kb)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"Hello @{message.from_user.username}", reply_markup=main_kb)



@dp.message(F.text == "🆘 Помощь")
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(f"Этот телеграм бот имеет толька две команды /help и /start")



@dp.message(Command("get_all_user"))
async def help(message: Message):
    users = await get_users()
    text = ""
    for user in users:
        text+= f"""
Username: {user['username']}  
Full name: {user['full_name']}
                             """
    await message.answer(text)

@dp.message(Command("add_task"))
async def add_task(message: Message, command: CommandObject):
    data = command.args
    data = data.split("/")
    if await create_task(data[0], data[1], data[2], message.from_user.id):
        await message.answer(f"Task with name {data[0]} created successful")
    else:
        await message.answer(f"Task with name {data[0]} get error in created")

        
@dp.message(F.text == "📋 Мои задачи")
@dp.message(Command("get_my_tasks"))
async def help(message: Message):
    tasks = await get_task_by_id(message.from_user.id)
    text = ""
    for task in tasks:
        text+= f"""
Id: {task['task_id']}  
Title: {task['title']}  
Caption: {task['caption']}
Dueration date: {task['due_date']}
Status: {task['status']}

Created at: {task['created_at']}


                             """
    await message.answer(text)

@dp.message(Command("update_task"))
async def update_task(message: Message, command: CommandObject):
    data = command.args
    data = data.split("/")
    if await update_task_db(data[0], data[1], data[2], data[3], message.from_user.id):
        await message.answer(f"Task with name {data[1]} update successful")
    else:
        await message.answer(f"Task with name {data[1]} get error in update")

@dp.message(Command("delete_task"))
async def delete_task(message: Message, command: CommandObject):
    data = command.args
    data = data.split("/")
    if await delete_task_db(data[0], message.from_user.id):
        await message.answer(f"Task with name {data[0]} delete successful")
    else:
        await message.answer(f"Task with name {data[0]} get error in delete")



async def main():
    await create_table()
    print("Bot started")
    await dp.start_polling(bot)
    
    
    
if __name__ == "__main__":
    asyncio.run(main())
