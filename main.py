import threading
import uvicorn
import bot, server
import os
from dotenv import load_dotenv
load_dotenv()

def run_bot():
    bot.clients.run(os.getenv('BOT_TOKEN'))

def run_server():
    uvicorn.run("server:app", host="0.0.0.0", port=8080)


t1 = threading.Thread(target=run_bot)
t2 = threading.Thread(target=run_server)

t1.start()
t2.start()

t1.join()
t2.join()