import os
from dotenv import load_dotenv
import discord
import random
import logging
from app import agent
from langchain_core.runnables import RunnableConfig

# Logging
logging.basicConfig(
    filename="logs/3d_printer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Load Bot's Token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    author_id = message.author.id
    user_input = message.content
    config: RunnableConfig = {"configurable": {"thread_id": f"discord_{author_id}"}}

    try:
        response = agent.invoke({"messages": user_input}, config)
        logging.info(f"Full Response: {response}")

        final_response = response["messages"][-1]
        logging.info(f"Final Response: {final_response}")
        await message.channel.send(final_response.content)

        logging.info(f"User: {user_input}")
        logging.info(f"Bot: {response}")

    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await message.channel.send("Maaf, terjadi kesalahan saat memproses permintaan Anda.")

if __name__ == "__main__":
    client.run(TOKEN)