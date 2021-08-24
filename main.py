import discord
import datetime
import asyncio
import markov
import os
import dotenv
import image_generator
from discord.ext import commands
from random import choice

env = dotenv.getenv()

current_path = os.path.abspath(os.path.dirname(__file__))

# listing the available assets
images = list(os.listdir(os.path.join(current_path, 'res/images')))
fonts = list(os.listdir(os.path.join(current_path, 'res/fonts')))

# initializing the markov chain
markov_chain = markov.markov(os.path.join(current_path,'res/idezetek'), 6)

def _get_random_image():
    return os.path.join(current_path, "res/images/" + choice(images))

def _get_duck_image(keywords):
    return image_generator.download_image(keywords)    
    
def _get_random_font():
    return os.path.join(current_path, "res/fonts/" + choice(fonts))

def _generate_quote_image():
    quote = markov_chain.generate_text()
    return (image_generator.generate(_get_random_image(), _get_random_font(), quote))

def _create_quote_image(user_text):
    return (image_generator.generate(_get_random_image(), _get_random_font(), user_text))

def _create_custom_quote_image(user_text, keywords):
    duck_image = _get_duck_image(keywords)
    if not duck_image:
        return None
    generated_image = image_generator.generate(_get_duck_image(keywords), _get_random_font(), user_text)
    os.remove(duck_image)
    return generated_image

client = commands.Bot(command_prefix="léci ")

@client.event
async def on_ready():
    print("A bot elérhető!")

@client.command(aliases=["motiváció", "Motiváció"])
async def motivacio(ctx):
    response = _generate_quote_image()
    await ctx.send(file=discord.File(response))
    os.remove(response)

@client.command(aliases=["készít", "keszit", "Készíts", "készíts"])
async def keszits(ctx, user_text, search_terms=None):

    if not search_terms:
        response = _create_quote_image(user_text)
    else:
        response = _create_custom_quote_image(user_text, search_terms)
        if not response:
            await ctx.send("Nincs találat :(")
            return

    await ctx.send(file=discord.File(response))
    os.remove(response)

if __name__ == "__main__":
    client.run(env.get("DISCORD_TOKEN"))
