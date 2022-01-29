from pyrogram import *
from config import Config
from pyrogram import Client, filters
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive import *
from os import path

DRIVE=Config.DRIVE

OWNER=Config.OWNER
gauth = GoogleAuth()




#Auth Drive access
@Client.on_message(filters.command("auth") &filters.text &filters.incoming  & filters.private )
async def auth(bot, message):

        if str(message.from_user.id) != OWNER:
            await message.reply_text("You are not my Master")
            return
        
        if path.exists("credentials.json"):
            await bot.send_message(chat_id=OWNER, text="you have already authenticated")
            return            
        else:
            auth_url = gauth.GetAuthUrl()
            await message.reply_text(f'To Get verification Code "\n" CLICK THE URL:{auth_url}')
            await message.reply_text(f"Replay your Auth code by typing /code <code>")
            return



@Client.on_message(filters.text &filters.incoming &filters.command("code") & filters.private )
async def code(bot, message): 
    text = message.text
    cmd, token = text.split(' ')         
    code = token
    try:
        gauth.Auth(code)
        gauth.SaveCredentialsFile('credentials.json') # Save the credentials
        drive = GoogleDrive(gauth)
        gfile = drive.CreateFile({'parents' : [{'id' : DRIVE}], 'title' : f'.Temp.txt'}) #where the files will be uploaded
        gfile.Upload() #upload
        await message.reply_text("Authentication Successful")        
    except:
        await message.reply_text("Invalid Code")
        return
