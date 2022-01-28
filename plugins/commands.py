from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from config import Config
import asyncio
import sys
import os
from helper.drive_utils.gdrive import *
from helper.authorize import *

USER=Config.USER
OWNER=Config.OWNER
HOME_TEXT=Config.HOME_TEXT
HOME_TEXT_OWNER=Config.HOME_TEXT_OWNER
HELP=Config.HELP
STATUS=Config.STATUS


#check alive "Start"
@Client.on_message(filters.command("igstart") & filters.group)
async def start(bot, cmd):
	OWNER =  Auth_user.owner(cmd.from_user.id)
	if str(cmd.from_user.id) != OWNER:	
		await cmd.reply_text(
			HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id, USER, USER, USER, OWNER), 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122")
					],
                    [
                        InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
						InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
                    ],
                    [
                        InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin"),
						InlineKeyboardButton("⚙️Update Channel", url="https://t.me/subin_works")

                    ]
					
				]
			)
		)
	else:
		await cmd.reply_text(
			HOME_TEXT_OWNER.format(cmd.from_user.first_name, cmd.from_user.id), 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122"),
					],
                    [
                        InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot")
                    ],
                    [
                        InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin"),
						InlineKeyboardButton("⚙️Update Channel", url="https://t.me/subin_works")

                    ]
					
				]
			)
		)

#help and restart
@Client.on_message(filters.command("ighelp") & filters.group)
async def help(bot, cmd):
	await cmd.reply_text(
		HELP,
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
					InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122"),
					InlineKeyboardButton("⚙️Update Channel", url="https://t.me/subin_works")
					
				],
				[
					InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
					InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
				]
			]
			)
		)

@Client.on_message(filters.command("igrestart") & filters.group)
async def stop(bot, cmd):
	if str(cmd.from_user.id) != OWNER:	
		await cmd.reply_text(
			HOME_TEXT.format(cmd.from_user.first_name, cmd.from_user.id, USER, USER, USER, OWNER), 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Other Bots", url="https://t.me/subin_works/122")	
					],
                    [
                        InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
						InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
                    ],
                    [
                        InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin"),
						InlineKeyboardButton("⚙️Update Channel", url="https://t.me/subin_works")

                    ]
					
				]
			)
		)
		return
	msg = await bot.send_message(
		text="Restarting your bot..",
		chat_id=cmd.from_user.id
		)
	await asyncio.sleep(2)
	await msg.edit("All Processes Stopped and Restarted")
	os.execl(sys.executable, sys.executable, *sys.argv)
