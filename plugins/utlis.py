import re
from config import Config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.tg_utils import *
from instaloader import Profile
from helper.drive_utils.gdrive import *
from helper.authorize import *

USER=Config.USER
OWNER=Config.OWNER
GROUP=Config.GROUP
AUTH=Config.AUTH
HOME_TEXT=Config.HOME_TEXT
HELP=Config.HELP
TUP= Config.TUP
STATUS=Config.STATUS
insta = Config.L

session=f"./{USER}"

@Client.on_message(filters.command("account") & filters.group)
async def account(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, int(GROUP)), 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Modder", url="https://t.me/query_realm"),
                        
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
		)
        return
    if 1 in STATUS:
        m=await message.reply_text("Getting Your data")
        try:
            profile = Profile.own_profile(insta.context)
            mediacount = profile.mediacount
            name = profile.full_name
            bio = profile.biography
            profilepic = profile.profile_pic_url
            username = profile.username
            igtvcount = profile.igtvcount
            followers = profile.followers
            following = profile.followees
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Download My Profile Pic", callback_data=f"ppic#{username}")
                        
                    ],
                    [
                        InlineKeyboardButton("Download All My Post", callback_data=f"post#{username}"),
                        InlineKeyboardButton("Download All Tagged Posts", callback_data=f"tagged#{username}")
                    ],
                    [
                        InlineKeyboardButton("Download Posts In My Feed", callback_data=f"feed#{username}"),
                        InlineKeyboardButton("Download My Saved Posts", callback_data=f"saved#{username}")
                    ],
                    [
                        InlineKeyboardButton("Download My IGTV Posts", callback_data=f"igtv#{username}"),
                        InlineKeyboardButton("Download My Highlights", callback_data=f"highlights#{username}")
                    ],
                    [
                        InlineKeyboardButton("Download My Stories ", callback_data=f"stories#{username}"),
                        InlineKeyboardButton("Download Stories of My Followees", callback_data=f"fstories#{username}")
                    ],
                    [
                        InlineKeyboardButton("Get a List Of My Followers", callback_data=f"followers#{username}"),
                        InlineKeyboardButton("Get a List Of My Followees", callback_data=f"followees#{username}")
                    ]

                ]
                )
            await m.delete()
            await bot.send_photo(
                        chat_id = GROUP,
                        photo=profilepic,
                        caption=f"🏷 **Name**: {name}\n🔖 **Username**: {profile.username}\n📝**Bio**: {bio}\n📍 **Account Type**: {acc_type(profile.is_private)}\n🏭 **Is Business Account?**: {yes_or_no(profile.is_business_account)}\n👥 **Total Followers**: {followers}\n👥 **Total Following**: {following}\n📸 **Total Posts**: {mediacount}\n📺 **IGTV Videos**: {igtvcount}",
                        reply_markup=reply_markup
                    )
        except Exception as e:
            await m.edit(e)

    else:
        await message.reply_text("You must login first by /login")

#get Ig user Data 
@Client.on_message(filters.text &filters.incoming &filters.command("ig") & filters.group )
async def ig(bot, message):
    GROUP = Auth_chat.search_chat(message.chat.id)
    AUTH = Auth_user.search_auth(message.from_user.id)
    if str(message.from_user.id) != AUTH:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, int(GROUP)),
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/subinps'),
						InlineKeyboardButton("🤖Modder", url="https://t.me/query_realm"),
                        
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
		)
        return
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m = await message.reply_text("Fetching data from Instagram🔗")
    chat_id= GROUP
    text = message.text
    cmd, username = text.split(' ')
    if "https://instagram.com/stories/" in username:
        await m.edit("Stories from links are not yet supported🥴\n\nYou can download stories from Username.")
        return

    link = r'^https://www\.instagram\.com/([A-Za-z0-9._]+/)?(p|tv|reel)/([A-Za-z0-9\-_]*)'
    result = re.search(link, username)
    
    if result:
        Post_type = {
            'p': 'POST',
            'tv': 'IGTV',
            'reel': 'REELS'
        }
        supported = Post_type.get(result.group(2))
        if not supported:
            await m.edit('Unsupported Format')
            return
        sent = await m.edit(f'`Fetching {supported} Content from Instagram.`')
        shortcode = result.group(3)
        try:
            userid=str(message.from_user.id)
            dir=f"{userid}/{shortcode}"
            chat_id= GROUP
            command = [
                "instaloader",
                "--no-metadata-json",
                "--no-compress-json",
                "--no-captions",
                "--no-video-thumbnails",
                "--filename-pattern={profile}_UTC_{date_utc}",
                "--login", USER,
                "-f", session,
                "--dirname-pattern", dir,
                "--", f"-{shortcode}"
                ]
            await download_insta(command, sent, dir)
            gid =None
            gid = gup(dir,gid)
            await bot.send_message(GROUP,f'The Drive Link: {gid}')
            if TUP == 'True':
                await upload(m, bot, chat_id, dir)
            else:
                pass

        except Exception as e:
            print(e)
            await bot.send_message(chat_id=GROUP, text=e)
            pass
    elif "https://" in username:
        await m.edit('Unsupported Format')
        return

    else:
        await m.edit(f"Fetching details for <code>@{username}</code>")
        try:
            profile = Profile.from_username(insta.context, username)
            mediacount = profile.mediacount
            name = profile.full_name
            profilepic = profile.profile_pic_url
            igtvcount = profile.igtvcount
            bio = profile.biography
            followers = profile.followers
            following = profile.followees
            is_followed = yes_or_no(profile.followed_by_viewer) 
            is_following = yes_or_no(profile.follows_viewer)
            type = acc_type(profile.is_private)
            if type == "🔒Private🔒" and is_followed == "No":
                print("reached")
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Download Profile Pic", callback_data=f"ppic#{username}"),
                        ]
                    ]
                )
            else:
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Profile Pic", callback_data=f"ppic#{username}")
                        ],
                        [
                            InlineKeyboardButton("All Post", callback_data=f"post#{username}"),
                            InlineKeyboardButton("All Tagged Posts", callback_data=f"tagged#{username}")
                        ],
                        [
                            InlineKeyboardButton("All IGTV", callback_data=f"igtv#{username}"),
                            InlineKeyboardButton("Stories ", callback_data=f"stories#{username}"),
                            InlineKeyboardButton("Highlights", callback_data=f"highlights#{username}")
                        ],
                        [
                            InlineKeyboardButton(f"{name}'s Followers", callback_data=f"followers#{username}"),
                            InlineKeyboardButton(f"{name}'s Followees", callback_data=f"followees#{username}")
                        ]
                    ]
                )
            await m.delete()
            try:
                await bot.send_photo(
                    chat_id = GROUP,
                    photo=profilepic,
                    caption=f"🏷 **Name**: {name}\n🔖 **Username**: {profile.username}\n📝 **Bio**: {bio}\n📍 **Account Type**: {acc_type(profile.is_private)}\n🏭 **Is Business Account?**: {yes_or_no(profile.is_business_account)}\n👥 **Total Followers**: {followers}\n👥 **Total Following**: {following}\n**👤 Is {name} Following You?**: {is_following}\n**👤 Is You Following {name} **: {is_followed}\n📸 **Total Posts**: {mediacount}\n📺 **IGTV Videos**: {igtvcount}",
                    reply_markup=reply_markup
                    )
            except Exception as e:
                print(e)
                await bot.send_message(chat_id, e)
        except Exception as e:
            print(e)
            await m.edit(e)
            pass