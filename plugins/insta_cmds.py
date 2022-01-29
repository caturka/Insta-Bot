from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from config import Config
from instaloader import Profile
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
import os
from helper.tg_utils import *
from helper.drive_utils.gdrive import *
from helper.authorize import *
import time 
from helper.SubFolRmv import *

AUTH=Config.AUTH
USER=Config.USER
OWNER=Config.OWNER
TUP= Config.TUP
GROUP=Config.GROUP
HOME_TEXT_OWNER=Config.HOME_TEXT_OWNER
HELP=Config.HELP
HOME_TEXT=Config.HOME_TEXT
session=f"./{USER}"
STATUS=Config.STATUS


insta = Config.L
buttons=InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
            InlineKeyboardButton("🤖Modder", url="https://t.me/query_realm")
        ],
        [
            InlineKeyboardButton("🔗Source Code", url="https://github.com/subinps/Instagram-Bot"),
            InlineKeyboardButton("🧩Deploy Own Bot", url="https://heroku.com/deploy?template=https://github.com/subinps/Instagram-Bot")
        ],
        [
            InlineKeyboardButton("👨🏼‍🦯How To Use?", callback_data="help#subin"),
            InlineKeyboardButton("Want Modded Code", url="https://t.me/query_realm")
        ]
					
    ]
    )




@Client.on_message(filters.command("posts") & filters.group)
async def post(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    await bot.send_message(
            GROUP,
            f"What type of post do you want to download?.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Pic+Videos", callback_data=f"photos#{username}"),
                        InlineKeyboardButton("ALL Posts", callback_data=f"video#{username}")
                    ]
                ]
            )
        )
    

@Client.on_message(filters.command("igtv") & filters.group)
async def igtv(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching IGTV from <code>@{username}</code>")
    profile = Profile.from_username(insta.context, username)
    igtvcount = profile.igtvcount
    await m.edit(
        text = f"Do you Want to download all IGTV posts?\nThere are {igtvcount} posts.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data=f"yesigtv#{username}"),
                    InlineKeyboardButton("No", callback_data=f"no#{username}")
                ]
            ]
        )
        )
    


@Client.on_message(filters.command("followers") & filters.group)
async def followers(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching Followers list of <code>@{username}</code>")
    chat_id=GROUP
    f = profile.get_followers()
    followers=f"**Followers List for {name}**\n\n"
    for p in f:
        followers += f"\n[{p.username}](www.instagram.com/{p.username})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"**Followers List for {name}**\n\n"
        f = profile.get_followers()
        for p in f:
            followers += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
        text_file = open(f"{username}'s followers.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s followers.txt", caption=f"{name}'s followers\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s followers.txt")


@Client.on_message(filters.command("followees") & filters.group)
async def followees(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching Followees list of <code>@{username}</code>")
    chat_id=GROUP
    f = profile.get_followees()
    followees=f"**Followees List for {name}**\n\n"
    for p in f:
        followees += f"\n[{p.username}](www.instagram.com/{p.username})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followees)
    except MessageTooLong:
        followees=f"**Followees List for {name}**\n\n"
        f = profile.get_followees()
        for p in f:
            followees += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
        text_file = open(f"{username}'s followees.txt", "w")
        text_file.write(followees)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s followees.txt", caption=f"{name}'s followees\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s followees.txt")




@Client.on_message(filters.command("fans") & filters.group)
async def fans(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching list of followees of <code>@{username}</code> who follows <code>@{username}</code>.")
    chat_id=GROUP
    f = profile.get_followers()
    fl = profile.get_followees()
    flist=[]
    fmlist=[]
    for fn in f:
        u=fn.username
        flist.append(u)
    for fm in fl:
        n=fm.username
        fmlist.append(n)

    fans = [value for value in fmlist if value in flist]
    print(len(fans))
    followers=f"**Fans List for {name}**\n\n"
    for p in fans:
        followers += f"\n[{p}](www.instagram.com/{p})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"**Fans List for {name}**\n\n"
        
        for p in fans:
            followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
        text_file = open(f"{username}'s fans.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s fans.txt", caption=f"{name}'s fans\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s fans.txt")


@Client.on_message(filters.command("notfollowing") & filters.group)
async def nfans(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching list of followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>.")
    chat_id=GROUP
    f = profile.get_followers()
    fl = profile.get_followees()
    flist=[]
    fmlist=[]
    for fn in f:
        u=fn.username
        flist.append(u)
    for fm in fl:
        n=fm.username
        fmlist.append(n)

    fans = list(set(fmlist) - set(flist))
    print(len(fans))
    followers=f"**Followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>**\n\n"
    for p in fans:
        followers += f"\n[{p}](www.instagram.com/{p})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"Followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>\n\n"
        for p in fans:
            followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
        text_file = open(f"{username}'s Non_followers.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s Non_followers.txt", caption=f"{name}'s Non_followers\n\nA Project By [XTZ_Bots](https://t.me/subin_works)")
        os.remove(f"./{username}'s Non_followers.txt")





@Client.on_message(filters.command("feed") & filters.group)
async def feed(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    count=None
    if " " in text:
        cmd, count = text.split(' ')
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m=await message.reply_text(f"Fetching Posts in Your Feed.")
    chat_id=GROUP
    dir=f"{OWNER}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    if count:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed",
            "--count", count
            ]
    else:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed"
            ]

    await download_insta(command, m, dir)
    # mod code
    await bot.send_message(chat_id,f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.")
    gid = None
    gid = gup(dir,gid)
    await  bot.send_message(GROUP,f'The Drive Link: {gid}')
    if TUP==True:
        await upload(m, bot, chat_id, dir)
    else:
        pass
        



@Client.on_message(filters.command("saved") & filters.group)
async def saved(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    count=None
    if " " in text:
        cmd, count = text.split(' ')
    m=await message.reply_text(f"Fetching your Saved Posts.")
    chat_id=GROUP
    dir=f"{OWNER}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    if count:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved",
            "--count", count
            ]
    else:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--filename-pattern={profile}_UTC_{date_utc}",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved"
            ]
    await download_insta(command, m, dir)
    # mod code
    await bot.send_message(chat_id,f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.")
    gid = None
    gid = gup(dir,gid)
    await  bot.send_message(GROUP,f'The Drive Link: {gid}')
    if TUP==True:
        await upload(m, bot, chat_id, dir)
    else:
        pass




@Client.on_message(filters.command("tagged") & filters.group)
async def tagged(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching the posts in which <code>@{username}</code> is tagged.")
    chat_id=GROUP
    dir=f"{OWNER}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--tagged",
        "--no-captions",
        "--no-video-thumbnails",
        "--filename-pattern={profile}_UTC_{date_utc}",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    # mod code
    await bot.send_message(chat_id,f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.")
    gid = None
    gid = gup(dir,gid)
    await  bot.send_message(GROUP,f'The Drive Link: {gid}')
    if TUP==True:
        await upload(m, bot, chat_id, dir)
    else:
        pass




@Client.on_message(filters.command("story") & filters.group)
async def story(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching stories of <code>@{username}</code>")
    chat_id=GROUP
    dir=f"{OWNER}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--stories",
        "--no-captions",
        "--no-video-thumbnails",
        "--filename-pattern={profile}_UTC_{date_utc}",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    # mod code
    await bot.send_message(chat_id,f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.")
    gid = None
    gid = gup(dir,gid)
    await  bot.send_message(GROUP,f'The Drive Link: {gid}')
    if TUP==True:
        await upload(m, bot, chat_id, dir)
    else:
        pass



@Client.on_message(filters.command("stories") & filters.group)
async def stories(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m=await message.reply_text(f"Fetching stories of all your followees")
    chat_id=GROUP
    dir=f"{OWNER}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-captions",
        "--no-posts",
        "--no-video-thumbnails",
        "--filename-pattern={profile}_UTC_{date_utc}",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        ":stories"
        ]
    await download_insta(command, m, dir)
    # mod code
    await bot.send_message(chat_id,f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.")
    gid = None
    gid = gup(dir,gid)
    await  bot.send_message(GROUP,f'The Drive Link: {gid}')
    if TUP==True:
        await upload(m, bot, chat_id, dir)
    else:
        pass





@Client.on_message(filters.command("highlights") & filters.group)
async def highlights(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, AUTH),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    text=message.text
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("Sorry!\nI can't fetch details from that account.\nSince its a Private account and you are not following <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching highlights from profile <code>@{username}</code>")
    chat_id=GROUP
    dir=f"{OWNER}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--highlights",
        "--no-captions",
        "--no-video-thumbnails",
        "--filename-pattern={profile}_UTC_{date_utc}",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    # mod code
    subdir= f"{OWNER}/{username}/{username}"
    rmv(subdir)
    await bot.send_message(chat_id,f"Drive Upload Starts, Please Wait....!\nThis may take longer time Depending upon number of posts.")
    gid = None
    gid = gup(dir,gid)
    await  bot.send_message(GROUP,f'The Drive Link: {gid}')
    if TUP==True:
        await upload(m, bot, chat_id, dir)
    else:
        pass
