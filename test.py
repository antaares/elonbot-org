import random
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# Replace YOUR_BOT_TOKEN with your actual bot token
bot = Bot(token='5768627444:AAH7uVRkUTruljr8jMKZu9AWzH68Uy4_v68')
dp = Dispatcher(bot)

# English words and sample sentences
words = {
    'apple': ['I ate an apple for breakfast.', 'The apple was juicy and delicious.'],
    'cat': ['The cat is sleeping on the couch.', 'I love playing with my cat.'],
    'book': ['I read a book before going to bed.', 'The book was so good I finished it in one day.'],
    # Add more words and sentences as needed
}

async def send_word_and_sentences():
    # Choose a random word and its sentences
    word, sentences = random.choice(list(words.items()))
    sentence1, sentence2 = sentences

    # Create a message with the word and sentences
    message = f"Word of the hour: {word}\n\n1. {sentence1}\n\n2. {sentence2}"

    # Send the message to the user
    user_id = 1393139047  # Replace with your actual user ID
    await bot.send_message(chat_id=user_id, text=message)

async def schedule_hourly():
    while True:
        await send_word_and_sentences()
        await asyncio.sleep(10)  # Send message every hour

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_hourly())
    executor.start_polling(dp, skip_updates=True)
