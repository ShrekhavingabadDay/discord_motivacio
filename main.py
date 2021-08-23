import discord
import datetime
import asyncio
import markov
import os
import dotenv
import image_generator
from random import choice

env = dotenv.getenv()

current_path = os.path.abspath(os.path.dirname(__file__))

# listing the available assets
images = list(os.listdir(os.path.join(current_path, 'res/images')))
fonts = list(os.listdir(os.path.join(current_path, 'res/fonts')))

# initializing the markov chain
markov_chain = markov.markov(os.path.join(current_path,'res/idezetek'), 6)

def _create_image():

    chosen_image_path = os.path.join(current_path, "res/images/" + choice(images))
    chosen_font_path = os.path.join(current_path, "res/fonts/" + choice(fonts))
    quote = markov_chain.generate_text()

    return (image_generator.generate(chosen_image_path, chosen_font_path, quote))

client = discord.Client()

@client.event
async def on_message(message):

    if message.content == "idézet pls":
        response = _create_image()
        await message.channel.send(file=discord.File(response))
        os.remove(response)

client.run(env.get("DISCORD_TOKEN"))
