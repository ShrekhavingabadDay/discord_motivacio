import discord
from discord.ext import commands
import datetime
import asyncio
import markov
import os
import image_generator
from random import choice

client = commands.bot()

current_path = os.path.abspath(os.path.dirname(__file__))

# listing the available assets
images = list(os.listdir(os.path.join(current_path, 'res/images')))
fonts = list(os.listdir(os.path.join(current_path, 'res/fonts')))

# initializing the markov chain
markov_chain = markov.markov(os.path.join(current_path,'res/idezetek'), 8)


def handle_request():

    chosen_image_path = os.path.join(current_path, "res/images/" + choice(images))
    chosen_font_path = os.path.join(current_path, "res/fonts/" + choice(fonts))
    quote = markov_chain.generate_text()

    image_generator.generate(chosen_image_path, chosen_font_path, quote)


