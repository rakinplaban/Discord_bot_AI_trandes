from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
# import bot
# import os
# from dotenv import load_dotenv

# load_dotenv()

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def root():
    # bot.clients.run(os.getenv('BOT_TOKEN'))
    return "Synthia is alive"

# if __name__=='__main__':
    
