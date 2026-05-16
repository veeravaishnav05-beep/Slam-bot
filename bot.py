# =========================================================
# 🔥 PREMIUM TELEGRAM ADMIN BOT
# FULL WORKING LUXURY EDITION - RAILWAY READY
# =========================================================

import telebot
from telebot.types import *
import time
from datetime import datetime
import traceback

# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = "8425853112:AAGT0VaNE15Dnj5EF2SvNu-mT7UOggyc3Ss"
ADMIN_ID = 8533061461

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Remove any existing webhook to use polling
bot.remove_webhook()
time.sleep(0.5)

# =========================================================
# DATABASE
# =========================================================

users_db = {}          # {user_id: {"username": str, "join_date": datetime}}
paid_users = set()
message_count = 0
bot_start_time = time.time()
bot_mode = True        # True = ON, False = OFF

# Welcome
welcome_text = ""
welcome_media = None
welcome_media_type = None
welcome_file = None
welcome_file_title = ""

# Custom messages
custom_messages = []

# Setup
setup_media = None
setup_media_type = None
setup_title = ""

# Broadcast
broadcast_data = None
broadcast_type = None
broadcast_title = ""

# Demo
demo_list = []          # [{"type":, "file_id":, "title":}]
demo_temp = []

# User custom buttons
user_buttons = []       # [{"name":, "type":, "file_id":}]

# Forward & join (only usernames like @channel)
group_forward_link = None
join_required_link = None
join_required_message = None

# Logo
bot_logo = None

# State
state = {}              # general state
settings_state = {}     # settings sub-state
temp_data = {}          # temporary storage

# =========================================================
# KEYBOARDS
# =========================================================

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.row("🚀 Startup", "⚙ Setup")
main_kb.row("🎭 Demo", "📡 Bot Status")
main_kb.row("📢 Broadcast", "🔧 Settings")
main_kb.row("⚡ Advance Tools")

startup_kb = ReplyKeyboardMarkup(resize_keyboard=True)
startup_kb.row("💬 Wel Msg", "📦 Wel Apk/File")
startup_kb.row("📝 Cstm Msg")
startup_kb.row("🏠 Main Menu")

demo_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
demo_admin_kb.row("🆕 New Demo", "📂 Old Demo")
demo_admin_kb.row("🗑 Remove All Demos")
demo_admin_kb.row("🏠 Main Menu")

demo_adding_kb = ReplyKeyboardMarkup(resize_keyboard=True)
demo_adding_kb.row("✅ DONE")
demo_adding_kb.row("🏠 Main Menu")

settings_kb = ReplyKeyboardMarkup(resize_keyboard=True)
settings_kb.row("🤖 BOT MODE", "🔘 BUTTONS")
settings_kb.row("📌 AVL BUTTON", "🔗 GROUP LINK")
settings_kb.row("🚪 JOIN RQD", "💀 DEL BOT")
settings_kb.row("🏠 Main Menu")

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_uptime():
    delta = time.time() - bot_start_time
    days = int(delta // 86400)
    hours = int((delta % 86400) // 3600)
    minutes = int((delta % 3600) // 60)
    seconds = int(delta % 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def today_users_count():
    today = datetime.now().date()
    count = 0
    for uid, data in users_db.items():
        if data.get("join_date") and data["join_date"].date() == today:
            count += 1
    return count

def send_welcome_to_user(uid):
    try:
        if welcome_media:
            if welcome_media_type == "photo":
                bot.send_photo(uid, welcome_media, caption=welcome_text or None)
            elif welcome_media_type == "video":
                bot.send_video(uid, welcome_media, caption=welcome_text or None)
        elif welcome_text:
            bot.send_message(uid, welcome_text)
        if welcome_file:
            bot.send_document(uid, welcome_file, caption=welcome_file_title or None)
        for msg in custom_messages:
            try:
                bot.send_message(uid, msg)
            except:
                pass
        # Show user buttons & demo
        user_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for btn in user_buttons:
            user_kb.row(btn["name"])
        if demo_list:
            user_kb.row("🎬 𝗩𝗶𝗲𝘄 𝗗𝗲𝗺𝗼")
        if user_buttons or demo_list:
            bot.send_message(uid, "💎 <b>𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗠𝗘𝗡𝗨</b>", reply_markup=user_kb)
    except Exception as e:
        print(f"Welcome error: {e}")

def send_join_required(uid):
    if not join_required_link or not join_required_message:
        return
    username = join_required_link.replace("@", "")
    url = f"https://t.me/{username}"
    buttons = InlineKeyboardMarkup()
    buttons.row(InlineKeyboardButton("🚀 𝗝𝗢𝗜𝗡 𝗡𝗢𝗪", url=url))
    try:
        bot.send_message(uid, join_required_message, reply_markup=buttons)
    except:
        pass

def is_user_member(uid, link):
    try:
        username = link.replace("@", "")
        member = bot.get_chat_member(f"@{username}", uid)
        return member.status not in ['left', 'kicked', 'banned']
    except:
        return False

# =========================================================
# START COMMAND
# =========================================================

@bot.message_handler(commands=['start'])
def start_command(message):
    global message_count
    try:
        message_count += 1
        uid = message.chat.id
        username = message.from_user.username or message.from_user.first_name
        if uid not in users_db:
            users_db[uid] = {"username": username, "join_date": datetime.now()}
        else:
            users_db[uid]["username"] = username

        state.pop(uid, None)
        settings_state.pop(uid, None)

        # ADMIN
        if uid == ADMIN_ID:
            txt = "🔥 <b>𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟</b>\n▰▰▰▰▰▰▰▰▰▰\n\n"
            if bot_mode:
                txt += "✅ <b>System:</b> ONLINE\n✅ <b>Security:</b> ACTIVE\n✅ <b>Control:</b> VERIFIED"
            else:
                txt += "⚠️ <b>BOT MODE:</b> OFF"
            bot.send_message(uid, txt, reply_markup=main_kb)
            return

        # USER SIDE
        if not bot_mode:
            return

        # Join required check
        if join_required_link:
            if not is_user_member(uid, join_required_link):
                send_join_required(uid)
                return

        send_welcome_to_user(uid)
    except Exception as e:
        print(f"Start error: {e}\n{traceback.format_exc()}")

# =========================================================
# MAIN MENU
# =========================================================

@bot.message_handler(func=lambda m: m.text == "🏠 Main Menu")
def main_menu_handler(message):
    try:
        state.pop(message.chat.id, None)
        settings_state.pop(message.chat.id, None)
        start_command(message)
    except Exception as e:
        print(f"Main menu error: {e}")

# ---------- STARTUP ----------
@bot.message_handler(func=lambda m: m.text == "🚀 Startup")
def startup_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        bot.send_message(message.chat.id,
                         "🚀 <b>𝗦𝗧𝗔𝗥𝗧𝗨𝗣 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 𝗖𝗘𝗡𝗧𝗘𝗥</b>\n▰▰▰▰▰▱▱▱▱▱\n✅ 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗦𝗬𝗦𝗧𝗘𝗠 𝗥𝗘𝗔𝗗𝗬\n👇 <b>CLICK BUTTONS</b>",
                         reply_markup=startup_kb)
    except Exception as e:
        print(f"Startup error: {e}")

# Welcome message
@bot.message_handler(func=lambda m: m.text == "💬 Wel Msg")
def welcome_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("📂 𝗢𝗟𝗗", callback_data="welcome_old"),
               InlineKeyboardButton("🆕 𝗡𝗘𝗪", callback_data="welcome_new"))
        kb.row(InlineKeyboardButton("🗑 𝗥𝗘𝗠𝗢𝗩𝗘", callback_data="welcome_remove"))
        bot.send_message(message.chat.id, "💬 <b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗠𝗔𝗡𝗔𝗚𝗘𝗥</b>\n👇 WHAT YOU WANT ?", reply_markup=kb)
    except Exception as e:
        print(f"Welcome panel error: {e}")

# Welcome file
@bot.message_handler(func=lambda m: m.text == "📦 Wel Apk/File")
def file_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        state[message.chat.id] = "waiting_file"
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("🗑 𝗥𝗘𝗠𝗢𝗩𝗘", callback_data="file_remove"))
        bot.send_message(message.chat.id, "📦 <b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗙𝗜𝗟𝗘</b>\n📤 SEND APK/FILE NOW", reply_markup=kb)
    except Exception as e:
        print(f"File panel error: {e}")

# Custom messages
@bot.message_handler(func=lambda m: m.text == "📝 Cstm Msg")
def custom_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("📂 𝗢𝗟𝗗", callback_data="custom_old"),
               InlineKeyboardButton("🆕 𝗡𝗘𝗪", callback_data="custom_new"))
        kb.row(InlineKeyboardButton("🗑 𝗥𝗘𝗠𝗢𝗩𝗘 𝗔𝗟𝗟", callback_data="custom_remove_all"))
        bot.send_message(message.chat.id, "📝 <b>𝗖𝗨𝗦𝗧𝗢𝗠 𝗠𝗦𝗚 𝗠𝗔𝗡𝗔𝗚𝗘𝗥</b>\n👇 WHAT YOU WANT ?", reply_markup=kb)
    except Exception as e:
        print(f"Custom panel error: {e}")

# Setup
@bot.message_handler(func=lambda m: m.text == "⚙ Setup")
def setup_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("📂 𝗢𝗟𝗗", callback_data="setup_old"),
               InlineKeyboardButton("🆕 𝗡𝗘𝗪", callback_data="setup_new"))
        bot.send_message(message.chat.id, "⚙ <b>𝗦𝗘𝗧𝗨𝗣 𝗖𝗢𝗡𝗧𝗥𝗢𝗟</b>\n👇 WHAT YOU WANT ?", reply_markup=kb)
    except Exception as e:
        print(f"Setup panel error: {e}")

# Broadcast
@bot.message_handler(func=lambda m: m.text == "📢 Broadcast")
def broadcast_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        state[message.chat.id] = "waiting_broadcast"
        bot.send_message(message.chat.id, "📢 <b>𝗕𝗥𝗢𝗔𝗗𝗖𝗔𝗦𝗧 𝗖𝗢𝗡𝗧𝗥𝗢𝗟</b>\n📩 SEND ANYTHING")
    except Exception as e:
        print(f"Broadcast panel error: {e}")

# Demo panel
@bot.message_handler(func=lambda m: m.text == "🎭 Demo")
def demo_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        global demo_temp
        demo_temp = []
        state.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "🎭 <b>𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗗𝗘𝗠𝗢 𝗦𝗧𝗨𝗗𝗜𝗢</b>\n✨ WHAT YOU WANT ?", reply_markup=demo_admin_kb)
    except Exception as e:
        print(f"Demo panel error: {e}")

@bot.message_handler(func=lambda m: m.text == "🆕 New Demo")
def new_demo(message):
    try:
        if message.chat.id != ADMIN_ID: return
        global demo_temp
        demo_temp = []
        state[message.chat.id] = "waiting_demo"
        bot.send_message(message.chat.id, "🎬 <b>𝗡𝗘𝗪 𝗗𝗘𝗠𝗢 𝗖𝗥𝗘𝗔𝗧𝗢𝗥</b>\n📤 Send anything\nPress DONE when finished", reply_markup=demo_adding_kb)
    except Exception as e:
        print(f"New demo error: {e}")

@bot.message_handler(func=lambda m: m.text == "📂 Old Demo")
def old_demo(message):
    try:
        if message.chat.id != ADMIN_ID: return
        if not demo_list:
            bot.send_message(message.chat.id, "❌ No demos found")
            return
        bot.send_message(message.chat.id, f"📂 <b>𝗦𝗔𝗩𝗘𝗗 𝗗𝗘𝗠𝗢𝗦 : {len(demo_list)}</b>")
        for i, d in enumerate(demo_list):
            kb = InlineKeyboardMarkup()
            kb.row(InlineKeyboardButton(f"🗑 Remove {i+1}", callback_data=f"demo_remove_{i}"))
            cap = f"📌 Demo {i+1}\n🏷 {d.get('title','No Title')}"
            if d['type'] == 'text':
                bot.send_message(message.chat.id, f"{cap}\n\n{d['file_id']}", reply_markup=kb)
            elif d['type'] == 'photo':
                bot.send_photo(message.chat.id, d['file_id'], caption=cap, reply_markup=kb)
            elif d['type'] == 'video':
                bot.send_video(message.chat.id, d['file_id'], caption=cap, reply_markup=kb)
            elif d['type'] == 'document':
                bot.send_document(message.chat.id, d['file_id'], caption=cap, reply_markup=kb)
    except Exception as e:
        print(f"Old demo error: {e}")

@bot.message_handler(func=lambda m: m.text == "🗑 Remove All Demos")
def remove_all_demos(message):
    try:
        if message.chat.id != ADMIN_ID: return
        if not demo_list:
            bot.send_message(message.chat.id, "❌ No demos")
            return
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("⚠ CONFIRM", callback_data="demo_remove_all_confirm"),
               InlineKeyboardButton("❌ CANCEL", callback_data="demo_remove_all_cancel"))
        bot.send_message(message.chat.id, f"⚠ Remove all {len(demo_list)} demos?", reply_markup=kb)
    except Exception as e:
        print(f"Remove all demos error: {e}")

@bot.message_handler(func=lambda m: m.text == "✅ DONE")
def demo_done(message):
    try:
        if message.chat.id != ADMIN_ID: return
        if state.get(message.chat.id) != "waiting_demo": return
        global demo_temp, demo_list
        if not demo_temp:
            bot.send_message(message.chat.id, "❌ No demos added", reply_markup=demo_admin_kb)
            state.pop(message.chat.id, None)
            return
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("✅ DONE", callback_data="demo_confirm_done"),
               InlineKeyboardButton("❌ CANCEL", callback_data="demo_confirm_cancel"))
        summary = "📊 <b>𝗗𝗘𝗠𝗢 𝗦𝗨𝗠𝗠𝗔𝗥𝗬</b>\n"
        for i, d in enumerate(demo_temp):
            summary += f"📌 Demo {i+1}: {d['type'].upper()} | {d.get('title','No Title')}\n"
        summary += f"\n📦 Total: {len(demo_temp)}"
        bot.send_message(message.chat.id, summary, reply_markup=kb)
        state[message.chat.id] = "waiting_demo_confirm"
    except Exception as e:
        print(f"Demo done error: {e}")

# =========================================================
# BOT STATUS
# =========================================================

@bot.message_handler(func=lambda m: m.text == "📡 Bot Status")
def bot_status(message):
    try:
        if message.chat.id != ADMIN_ID: return
        loading = bot.send_message(message.chat.id, "▱▱▱▱▱▱▱▱▱▱ 0%")
        for i in range(1,6):
            time.sleep(0.4)
            bar = "▰"*(i*2) + "▱"*(10-i*2)
            try:
                bot.edit_message_text(f"<b>{bar} {i*10}%</b>", message.chat.id, loading.message_id)
            except:
                pass
        total_users = len(users_db)
        total_admins = 1
        total_paid = len(paid_users)
        today = today_users_count()
        uptime = get_uptime()
        dm = message_count
        stats = (
            "📡 <b>𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦</b>\n"
            "▰▰▰▰▰▰▰▰▰▰\n"
            f"👥 Total Users: {total_users}\n"
            f"👑 Admins: {total_admins}\n"
            f"💎 Paid Users: {total_paid}\n"
            f"📅 Today: {today}\n"
            f"⏰ Uptime: {uptime}\n"
            f"💬 Total DMs: {dm}"
        )
        if bot_logo:
            try:
                bot.send_photo(message.chat.id, bot_logo, caption=stats)
            except:
                bot.send_message(message.chat.id, stats)
        else:
            bot.send_message(message.chat.id, stats)
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("📋 𝗨𝗦𝗘𝗥 𝗟𝗜𝗦𝗧", callback_data="userlist_download"))
        bot.send_message(message.chat.id, "<i>Download user data</i>", reply_markup=kb)
    except Exception as e:
        print(f"Bot status error: {e}")

# =========================================================
# SETTINGS
# =========================================================

@bot.message_handler(func=lambda m: m.text == "🔧 Settings")
def settings_panel(message):
    try:
        if message.chat.id != ADMIN_ID: return
        loading = bot.send_message(message.chat.id, "⚙️ <b>Loading Settings...</b>")
        time.sleep(2)
        bot.delete_message(message.chat.id, loading.message_id)
        bot.send_message(message.chat.id, "🔧 <b>𝗕𝗢𝗧 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 𝗠𝗢𝗗𝗘 ☠️🧡</b>\n▰▰▰▰▰▰▰▰▰▰", reply_markup=settings_kb)
    except Exception as e:
        print(f"Settings panel error: {e}")

# =========================================================
# SETTINGS SUB HANDLERS
# =========================================================

@bot.message_handler(func=lambda m: m.text == "🤖 BOT MODE" and m.chat.id == ADMIN_ID)
def botmode_handler(message):
    try:
        global bot_mode
        kb = InlineKeyboardMarkup()
        if bot_mode:
            kb.row(InlineKeyboardButton("🔴 𝗢𝗙𝗙 𝗕𝗢𝗧", callback_data="botmode_off"))
        else:
            kb.row(InlineKeyboardButton("🟢 𝗢𝗡 𝗕𝗢𝗧", callback_data="botmode_on"))
        state_text = "ON" if bot_mode else "OFF"
        bot.send_message(message.chat.id, f"🤖 <b>𝗕𝗢𝗧 𝗠𝗢𝗗𝗘</b>\nCurrent: {state_text}", reply_markup=kb)
    except Exception as e:
        print(f"Bot mode error: {e}")

@bot.message_handler(func=lambda m: m.text == "🔘 BUTTONS" and m.chat.id == ADMIN_ID)
def buttons_handler(message):
    try:
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("🆕 𝗡𝗘𝗪", callback_data="userbtn_new"),
               InlineKeyboardButton("📂 𝗢𝗟𝗗", callback_data="userbtn_old"))
        bot.send_message(message.chat.id, "🔘 <b>𝗨𝗦𝗘𝗥 𝗕𝗨𝗧𝗧𝗢𝗡𝗦</b>\nWHAT YOU WANT ?", reply_markup=kb)
    except Exception as e:
        print(f"Buttons handler error: {e}")

@bot.message_handler(func=lambda m: m.text == "📌 AVL BUTTON" and m.chat.id == ADMIN_ID)
def avl_handler(message):
    try:
        if not user_buttons:
            bot.send_message(message.chat.id, "❌ No buttons. Create in BUTTONS first.")
            return
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        for b in user_buttons:
            kb.row(b['name'])
        kb.row("🏠 Main Menu")
        bot.send_message(message.chat.id, "📌 <b>𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 𝗕𝗨𝗧𝗧𝗢𝗡𝗦</b>\nSelect button to set content", reply_markup=kb)
        settings_state[message.chat.id] = "awaiting_avl_select"
    except Exception as e:
        print(f"AVL handler error: {e}")

@bot.message_handler(func=lambda m: m.text == "🔗 GROUP LINK" and m.chat.id == ADMIN_ID)
def grouplink_handler(message):
    try:
        global group_forward_link
        if group_forward_link:
            kb = InlineKeyboardMarkup()
            kb.row(InlineKeyboardButton("🗑 𝗥𝗘𝗠𝗢𝗩𝗘", callback_data="grouplink_remove"))
            bot.send_message(message.chat.id, f"🔗 <b>𝗔𝗟𝗥𝗘𝗔𝗗𝗬 𝗦𝗘𝗧</b>\n{group_forward_link}", reply_markup=kb)
        else:
            settings_state[message.chat.id] = "awaiting_group_link"
            bot.send_message(message.chat.id, "🔗 <b>Send group/channel username</b> (e.g., @mychannel)")
    except Exception as e:
        print(f"Group link handler error: {e}")

@bot.message_handler(func=lambda m: m.text == "🚪 JOIN RQD" and m.chat.id == ADMIN_ID)
def joinrqd_handler(message):
    try:
        global join_required_link, join_required_message
        if join_required_link:
            kb = InlineKeyboardMarkup()
            kb.row(InlineKeyboardButton("🆕 𝗡𝗘𝗪", callback_data="joinrqd_new"),
                   InlineKeyboardButton("🗑 𝗥𝗘𝗠𝗢𝗩𝗘", callback_data="joinrqd_remove"))
            bot.send_message(message.chat.id, f"🚪 <b>𝗝𝗢𝗜𝗡 𝗥𝗘𝗤𝗨𝗜𝗥𝗘𝗗</b>\nCurrent: {join_required_link}\nWHAT YOU WANT?", reply_markup=kb)
        else:
            settings_state[message.chat.id] = "awaiting_join_link"
            bot.send_message(message.chat.id, "🔗 <b>Send group/channel username</b> for join required")
    except Exception as e:
        print(f"Join RQD error: {e}")

@bot.message_handler(func=lambda m: m.text == "💀 DEL BOT" and m.chat.id == ADMIN_ID)
def delbot_handler(message):
    try:
        kb = InlineKeyboardMarkup()
        kb.row(InlineKeyboardButton("⚠️ 𝗖𝗢𝗡𝗙𝗜𝗥𝗠", callback_data="delbot_confirm"),
               InlineKeyboardButton("❌ 𝗖𝗔𝗡𝗖𝗘𝗟", callback_data="delbot_cancel"))
        bot.send_message(message.chat.id, "💀 <b>𝗗𝗘𝗟𝗘𝗧𝗘 𝗕𝗢𝗧?</b>\nThis will stop the bot completely.", reply_markup=kb)
    except Exception as e:
        print(f"Del bot error: {e}")

# =========================================================
# TEXT HANDLER (integrated)
# =========================================================

@bot.message_handler(content_types=['text'])
def text_handler(message):
    global message_count, users_db, custom_messages, user_buttons, group_forward_link, join_required_link, join_required_message
    global welcome_text, welcome_file_title, setup_title, broadcast_data, broadcast_type, broadcast_title
    global demo_temp, demo_list

    try:
        message_count += 1
        cid = message.chat.id
        text = message.text

        # ADMIN text flows
        if cid == ADMIN_ID:
            ss = settings_state.get(cid)
            st = state.get(cid)

            # Settings: Button name
            if ss == "awaiting_button_name":
                temp_data[cid] = {"button_name": text}
                settings_state[cid] = "awaiting_button_type"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("🖼 𝗜𝗠𝗔𝗚𝗘𝗦", callback_data="btn_type_photo"),
                       InlineKeyboardButton("🎥 𝗩𝗜𝗗𝗘𝗢", callback_data="btn_type_video"))
                kb.row(InlineKeyboardButton("📱 𝗔𝗣𝗣𝗦", callback_data="btn_type_document"),
                       InlineKeyboardButton("📄 𝗙𝗜𝗟𝗘𝗦", callback_data="btn_type_document"))
                bot.send_message(cid, f"✅ Name set: <b>{text}</b>\nSelect content type:", reply_markup=kb)
                return

            # Group link input
            if ss == "awaiting_group_link":
                link = text.strip()
                if link.startswith("https://") or link.startswith("t.me/"):
                    bot.send_message(cid, "❌ Please send only **username** like @mychannel")
                    return
                if not link.startswith("@"):
                    link = "@" + link
                temp_data[cid] = link
                settings_state[cid] = "awaiting_group_admin"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("✅ 𝗗𝗢𝗡𝗘", callback_data="groupadmin_done"),
                       InlineKeyboardButton("❌ 𝗖𝗔𝗡𝗖𝗘𝗟", callback_data="groupadmin_cancel"))
                bot.send_message(cid, f"🔗 Username: {link}\n<b>PLEASE MAKE BOT ADMIN IN THAT GROUP/CHANNEL THEN PRESS DONE</b>", reply_markup=kb)
                return

            # Join link input
            if ss == "awaiting_join_link":
                link = text.strip()
                if link.startswith("https://") or link.startswith("t.me/"):
                    bot.send_message(cid, "❌ Please send only **username** like @mychannel")
                    return
                if not link.startswith("@"):
                    link = "@" + link
                temp_data[cid] = link
                settings_state[cid] = "awaiting_join_message"
                bot.send_message(cid, "📝 <b>Send join required message</b>")
                return

            # Join message input
            if ss == "awaiting_join_message":
                join_required_link = temp_data.pop(cid)
                join_required_message = text
                settings_state.pop(cid, None)
                bot.send_message(cid, f"✅ Join requirement set!\nLink: {join_required_link}\nMessage: {text}", reply_markup=settings_kb)
                return

            # AVL select
            if ss == "awaiting_avl_select":
                found = None
                for i, b in enumerate(user_buttons):
                    if b['name'] == text:
                        found = i
                        break
                if found is not None:
                    temp_data[cid] = found
                    settings_state[cid] = "awaiting_avl_content"
                    bot.send_message(cid, f"📤 Send new content for button <b>{text}</b> ({user_buttons[found]['type']})")
                else:
                    bot.send_message(cid, "❌ Button not found. Use available buttons.")
                return

            # --- Welcome, custom, file flows ---
            if st == "waiting_welcome_text":
                welcome_text = text
                state[cid] = None
                bot.send_message(cid, "✅ Welcome message saved", reply_markup=startup_kb)
                return
            if st == "waiting_file_title":
                welcome_file_title = text
                state[cid] = None
                bot.send_message(cid, "✅ File title saved", reply_markup=startup_kb)
                return
            if st == "waiting_custom":
                custom_messages.append(text)
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES ADD MORE", callback_data="custom_add_more"),
                       InlineKeyboardButton("DONE", callback_data="custom_done"))
                bot.send_message(cid, f"✅ Added. Total: {len(custom_messages)}\nAdd more?", reply_markup=kb)
                return
            if st == "waiting_setup_title":
                setup_title = text
                state[cid] = None
                bot.send_message(cid, "✅ Setup saved", reply_markup=main_kb)
                return
            if st == "waiting_broadcast":
                broadcast_data = text
                broadcast_type = "text"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="broadcast_title_yes"),
                       InlineKeyboardButton("NO", callback_data="broadcast_title_no"))
                bot.send_message(cid, "Add title?", reply_markup=kb)
                return
            if st == "waiting_broadcast_title":
                broadcast_title = text
                state[cid] = None
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("DONE", callback_data="broadcast_confirm"),
                       InlineKeyboardButton("CANCEL", callback_data="broadcast_cancel"))
                bot.send_message(cid, "⚠ Confirm broadcast?", reply_markup=kb)
                return
            if st == "waiting_demo":
                demo_temp.append({"type":"text","file_id":text,"title":""})
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="demo_title_yes"),
                       InlineKeyboardButton("NO", callback_data="demo_title_no"))
                bot.send_message(cid, f"✅ Text demo added. Total: {len(demo_temp)}\nAdd title?", reply_markup=kb)
                return
            if st == "waiting_demo_title":
                if demo_temp:
                    demo_temp[-1]['title'] = text
                state[cid] = "waiting_demo"
                bot.send_message(cid, f"🏷 Title set: {text}\nSend more or DONE", reply_markup=demo_adding_kb)
                return
            if st == "waiting_demo_confirm":
                return

        # USER text: custom button triggers
        if cid != ADMIN_ID and bot_mode:
            for btn in user_buttons:
                if text == btn["name"]:
                    try:
                        if btn["type"] == "photo":
                            bot.send_photo(cid, btn["file_id"])
                        elif btn["type"] == "video":
                            bot.send_video(cid, btn["file_id"])
                        elif btn["type"] == "document":
                            bot.send_document(cid, btn["file_id"])
                    except:
                        bot.send_message(cid, "❌ Error loading content.")
                    return
            if text == "🎬 𝗩𝗶𝗲𝘄 𝗗𝗲𝗺𝗼":
                if demo_list:
                    bot.send_message(cid, "✨ <b>𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗗𝗘𝗠𝗢 𝗦𝗛𝗢𝗪𝗖𝗔𝗦𝗘</b>")
                    for i, d in enumerate(demo_list):
                        cap = f"🎬 Demo {i+1}" + (f"\n🏷 {d['title']}" if d.get('title') else "")
                        try:
                            if d['type'] == 'text':
                                bot.send_message(cid, f"{cap}\n\n{d['file_id']}")
                            elif d['type'] == 'photo':
                                bot.send_photo(cid, d['file_id'], caption=cap)
                            elif d['type'] == 'video':
                                bot.send_video(cid, d['file_id'], caption=cap)
                            elif d['type'] == 'document':
                                bot.send_document(cid, d['file_id'], caption=cap)
                        except:
                            pass
                    bot.send_message(cid, "✅ All demos shown 💎")
                else:
                    bot.send_message(cid, "❌ No demos available")
                return
    except Exception as e:
        print(f"Text handler error: {e}\n{traceback.format_exc()}")

# =========================================================
# PHOTO HANDLER
# =========================================================

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    global welcome_media, welcome_media_type, setup_media, setup_media_type, broadcast_data, broadcast_type
    global demo_temp, user_buttons
    try:
        cid = message.chat.id
        st = state.get(cid)
        ss = settings_state.get(cid)

        if cid == ADMIN_ID:
            if st == "waiting_welcome_media":
                welcome_media = message.photo[-1].file_id
                welcome_media_type = "photo"
                state[cid] = "waiting_welcome_text"
                bot.send_message(cid, "📸 Photo received. Send welcome message:")
                return
            if st == "waiting_setup":
                setup_media = message.photo[-1].file_id
                setup_media_type = "photo"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="setup_title_yes"),
                       InlineKeyboardButton("NO", callback_data="setup_title_no"))
                bot.send_message(cid, "Add title?", reply_markup=kb)
                return
            if st == "waiting_broadcast":
                broadcast_data = message.photo[-1].file_id
                broadcast_type = "photo"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="broadcast_title_yes"),
                       InlineKeyboardButton("NO", callback_data="broadcast_title_no"))
                bot.send_message(cid, "Add title?", reply_markup=kb)
                return
            if st == "waiting_demo":
                demo_temp.append({"type":"photo","file_id":message.photo[-1].file_id,"title":""})
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="demo_title_yes"),
                       InlineKeyboardButton("NO", callback_data="demo_title_no"))
                bot.send_message(cid, f"📸 Photo demo added. Total: {len(demo_temp)}\nAdd title?", reply_markup=kb)
                return
            # New button content
            if ss == "awaiting_button_content":
                btn_name = temp_data.get(cid, {}).get("button_name")
                if btn_name:
                    user_buttons.append({"name":btn_name, "type":"photo", "file_id":message.photo[-1].file_id})
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Button '{btn_name}' created with photo!", reply_markup=settings_kb)
                return
            # AVL content update
            if ss == "awaiting_avl_content":
                idx = temp_data.get(cid)
                if idx is not None and idx < len(user_buttons):
                    user_buttons[idx]["file_id"] = message.photo[-1].file_id
                    user_buttons[idx]["type"] = "photo"
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Content updated for {user_buttons[idx]['name']}", reply_markup=settings_kb)
                return

        # User forwarding
        if cid != ADMIN_ID and bot_mode and group_forward_link:
            try:
                bot.forward_message(group_forward_link, cid, message.message_id)
            except:
                pass
    except Exception as e:
        print(f"Photo handler error: {e}\n{traceback.format_exc()}")

# =========================================================
# VIDEO HANDLER
# =========================================================

@bot.message_handler(content_types=['video'])
def video_handler(message):
    global welcome_media, welcome_media_type, setup_media, setup_media_type, broadcast_data, broadcast_type
    global demo_temp, user_buttons
    try:
        cid = message.chat.id
        st = state.get(cid)
        ss = settings_state.get(cid)

        if cid == ADMIN_ID:
            if st == "waiting_welcome_media":
                welcome_media = message.video.file_id
                welcome_media_type = "video"
                state[cid] = "waiting_welcome_text"
                bot.send_message(cid, "🎥 Video received. Send welcome message:")
                return
            if st == "waiting_setup":
                setup_media = message.video.file_id
                setup_media_type = "video"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="setup_title_yes"),
                       InlineKeyboardButton("NO", callback_data="setup_title_no"))
                bot.send_message(cid, "Add title?", reply_markup=kb)
                return
            if st == "waiting_broadcast":
                broadcast_data = message.video.file_id
                broadcast_type = "video"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="broadcast_title_yes"),
                       InlineKeyboardButton("NO", callback_data="broadcast_title_no"))
                bot.send_message(cid, "Add title?", reply_markup=kb)
                return
            if st == "waiting_demo":
                demo_temp.append({"type":"video","file_id":message.video.file_id,"title":""})
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="demo_title_yes"),
                       InlineKeyboardButton("NO", callback_data="demo_title_no"))
                bot.send_message(cid, f"🎥 Video demo added. Total: {len(demo_temp)}\nAdd title?", reply_markup=kb)
                return
            if ss == "awaiting_button_content":
                btn_name = temp_data.get(cid, {}).get("button_name")
                if btn_name:
                    user_buttons.append({"name":btn_name, "type":"video", "file_id":message.video.file_id})
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Button '{btn_name}' created with video!", reply_markup=settings_kb)
                return
            if ss == "awaiting_avl_content":
                idx = temp_data.get(cid)
                if idx is not None and idx < len(user_buttons):
                    user_buttons[idx]["file_id"] = message.video.file_id
                    user_buttons[idx]["type"] = "video"
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Content updated for {user_buttons[idx]['name']}", reply_markup=settings_kb)
                return

        if cid != ADMIN_ID and bot_mode and group_forward_link:
            try:
                bot.forward_message(group_forward_link, cid, message.message_id)
            except:
                pass
    except Exception as e:
        print(f"Video handler error: {e}\n{traceback.format_exc()}")

# =========================================================
# DOCUMENT HANDLER
# =========================================================

@bot.message_handler(content_types=['document'])
def document_handler(message):
    global welcome_file, broadcast_data, broadcast_type, demo_temp, user_buttons
    try:
        cid = message.chat.id
        st = state.get(cid)
        ss = settings_state.get(cid)

        if cid == ADMIN_ID:
            if st == "waiting_file":
                welcome_file = message.document.file_id
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="file_title_yes"),
                       InlineKeyboardButton("NO", callback_data="file_title_no"))
                bot.send_message(cid, "Add file title?", reply_markup=kb)
                return
            if st == "waiting_broadcast":
                broadcast_data = message.document.file_id
                broadcast_type = "document"
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="broadcast_title_yes"),
                       InlineKeyboardButton("NO", callback_data="broadcast_title_no"))
                bot.send_message(cid, "Add title?", reply_markup=kb)
                return
            if st == "waiting_demo":
                demo_temp.append({"type":"document","file_id":message.document.file_id,"title":""})
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("YES", callback_data="demo_title_yes"),
                       InlineKeyboardButton("NO", callback_data="demo_title_no"))
                bot.send_message(cid, f"📄 Document demo added. Total: {len(demo_temp)}\nAdd title?", reply_markup=kb)
                return
            if ss == "awaiting_button_content":
                btn_name = temp_data.get(cid, {}).get("button_name")
                if btn_name:
                    user_buttons.append({"name":btn_name, "type":"document", "file_id":message.document.file_id})
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Button '{btn_name}' created with document!", reply_markup=settings_kb)
                return
            if ss == "awaiting_avl_content":
                idx = temp_data.get(cid)
                if idx is not None and idx < len(user_buttons):
                    user_buttons[idx]["file_id"] = message.document.file_id
                    user_buttons[idx]["type"] = "document"
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Content updated for {user_buttons[idx]['name']}", reply_markup=settings_kb)
                return

        if cid != ADMIN_ID and bot_mode and group_forward_link:
            try:
                bot.forward_message(group_forward_link, cid, message.message_id)
            except:
                pass
    except Exception as e:
        print(f"Document handler error: {e}\n{traceback.format_exc()}")

# =========================================================
# SINGLE CALLBACK HANDLER
# =========================================================

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global welcome_text, welcome_media, welcome_media_type, welcome_file, welcome_file_title
    global setup_media, setup_media_type, setup_title
    global broadcast_data, broadcast_type, broadcast_title
    global demo_list, demo_temp, user_buttons, bot_mode
    global group_forward_link, join_required_link, join_required_message
    global custom_messages

    try:
        cid = call.message.chat.id
        data = call.data
        bot.answer_callback_query(call.id)

        # Welcome
        if data == "welcome_old":
            if welcome_text:
                bot.send_message(cid, f"📜 Saved: {welcome_text}")
            else:
                bot.send_message(cid, "❌ No welcome")
        elif data == "welcome_new":
            kb = InlineKeyboardMarkup()
            kb.row(InlineKeyboardButton("YES", callback_data="welcome_media_yes"), InlineKeyboardButton("NO", callback_data="welcome_media_no"))
            bot.send_message(cid, "Image/Video?", reply_markup=kb)
        elif data == "welcome_media_yes":
            state[cid] = "waiting_welcome_media"
            bot.send_message(cid, "Send image/video")
        elif data == "welcome_media_no":
            state[cid] = "waiting_welcome_text"
            bot.send_message(cid, "Send welcome message")
        elif data == "welcome_remove":
            welcome_text = ""; welcome_media = None; welcome_media_type = None
            bot.send_message(cid, "🗑 Welcome removed")
        elif data == "file_remove":
            welcome_file = None; welcome_file_title = ""
            bot.send_message(cid, "🗑 File removed")
        elif data == "file_title_yes":
            state[cid] = "waiting_file_title"
            bot.send_message(cid, "Send file title")
        elif data == "file_title_no":
            state[cid] = None
            bot.send_message(cid, "✅ File saved", reply_markup=startup_kb)
        elif data == "custom_old":
            if not custom_messages:
                bot.send_message(cid, "❌ No custom messages")
            else:
                for i, m in enumerate(custom_messages):
                    kb = InlineKeyboardMarkup()
                    kb.row(InlineKeyboardButton("🗑 Remove", callback_data=f"custom_delete_{i}"))
                    bot.send_message(cid, f"📜 Msg {i+1}: {m}", reply_markup=kb)
        elif data == "custom_new":
            state[cid] = "waiting_custom"
            bot.send_message(cid, "Send custom message")
        elif data == "custom_remove_all":
            custom_messages.clear()
            bot.send_message(cid, "🗑 All custom removed")
        elif data.startswith("custom_delete_"):
            i = int(data.split("_")[-1])
            if i < len(custom_messages):
                custom_messages.pop(i)
                bot.send_message(cid, "🗑 Removed")
        elif data == "custom_add_more":
            state[cid] = "waiting_custom"
            bot.send_message(cid, "Send another")
        elif data == "custom_done":
            state[cid] = None
            bot.send_message(cid, f"✅ {len(custom_messages)} messages saved", reply_markup=startup_kb)
        elif data == "setup_old":
            if setup_media:
                kb = InlineKeyboardMarkup()
                kb.row(InlineKeyboardButton("🗑 Remove", callback_data="setup_remove"))
                cap = "📂 Setup" + (f"\n🏷 {setup_title}" if setup_title else "")
                if setup_media_type == "photo":
                    bot.send_photo(cid, setup_media, caption=cap, reply_markup=kb)
                else:
                    bot.send_video(cid, setup_media, caption=cap, reply_markup=kb)
            else:
                bot.send_message(cid, "❌ No setup")
        elif data == "setup_new":
            state[cid] = "waiting_setup"
            bot.send_message(cid, "Send image/video")
        elif data == "setup_remove":
            setup_media = None; setup_media_type = None; setup_title = ""
            bot.send_message(cid, "🗑 Setup removed")
        elif data == "setup_title_yes":
            state[cid] = "waiting_setup_title"
            bot.send_message(cid, "Send title")
        elif data == "setup_title_no":
            state[cid] = None
            bot.send_message(cid, "✅ Setup saved", reply_markup=main_kb)
        # Broadcast
        elif data == "broadcast_title_yes":
            state[cid] = "waiting_broadcast_title"
            bot.send_message(cid, "Send title")
        elif data == "broadcast_title_no":
            state[cid] = None
            kb = InlineKeyboardMarkup()
            kb.row(InlineKeyboardButton("DONE", callback_data="broadcast_confirm"), InlineKeyboardButton("CANCEL", callback_data="broadcast_cancel"))
            bot.send_message(cid, "Confirm broadcast?", reply_markup=kb)
        elif data == "broadcast_cancel":
            broadcast_data = None; broadcast_title = ""; broadcast_type = None
            bot.send_message(cid, "❌ Cancelled", reply_markup=main_kb)
        elif data == "broadcast_confirm":
            success = 0; failed = 0
            loading = bot.send_message(cid, "🚀 Broadcasting...")
            users = list(users_db.keys())
            for u in users:
                try:
                    if broadcast_type == "text":
                        msg = f"{broadcast_title}\n\n{broadcast_data}" if broadcast_title else broadcast_data
                        bot.send_message(u, msg)
                    elif broadcast_type == "photo":
                        bot.send_photo(u, broadcast_data, caption=broadcast_title or None)
                    elif broadcast_type == "video":
                        bot.send_video(u, broadcast_data, caption=broadcast_title or None)
                    elif broadcast_type == "document":
                        bot.send_document(u, broadcast_data, caption=broadcast_title or None)
                    success += 1
                except:
                    failed += 1
            broadcast_data = None; broadcast_title = ""; broadcast_type = None
            bot.edit_message_text(f"✅ Broadcast done\nSuccess: {success}\nFailed: {failed}\nUsers: {len(users)}", cid, loading.message_id)
        # Demo
        elif data == "demo_title_yes":
            state[cid] = "waiting_demo_title"
            bot.send_message(cid, "Send title for this demo")
        elif data == "demo_title_no":
            if demo_temp: demo_temp[-1]['title'] = ""
            bot.send_message(cid, f"✅ Demo saved without title. Total: {len(demo_temp)}\nSend more or DONE", reply_markup=demo_adding_kb)
        elif data == "demo_confirm_done":
            demo_list = list(demo_temp)
            demo_temp = []
            state[cid] = None
            bot.send_message(cid, f"🎉 {len(demo_list)} demos saved!", reply_markup=demo_admin_kb)
        elif data == "demo_confirm_cancel":
            demo_temp = []
            state[cid] = None
            bot.send_message(cid, "❌ Cancelled", reply_markup=demo_admin_kb)
        elif data.startswith("demo_remove_"):
            i = int(data.split("_")[-1])
            if i < len(demo_list):
                demo_list.pop(i)
                bot.send_message(cid, "🗑 Demo removed")
        elif data == "demo_remove_all_confirm":
            demo_list.clear()
            bot.send_message(cid, "🗑 All demos removed", reply_markup=demo_admin_kb)
        elif data == "demo_remove_all_cancel":
            bot.send_message(cid, "✅ Cancelled", reply_markup=demo_admin_kb)
        # Settings
        elif data == "userlist_download":
            lines = [f"{uid} | @{users_db[uid]['username']} | {users_db[uid]['join_date'].strftime('%Y-%m-%d %H:%M')}" for uid in users_db]
            txt = "\n".join(lines)
            bot.send_document(cid, InputFile(txt.encode('utf-8'), 'users.txt'), caption=f"Total: {len(users_db)}")
        elif data == "botmode_off":
            bot_mode = False
            bot.edit_message_text("🔴 Bot is now OFF", cid, call.message.message_id)
        elif data == "botmode_on":
            bot_mode = True
            bot.edit_message_text("🟢 Bot is now ON", cid, call.message.message_id)
        elif data == "userbtn_new":
            settings_state[cid] = "awaiting_button_name"
            bot.send_message(cid, "Send button name")
        elif data == "userbtn_old":
            if not user_buttons:
                bot.send_message(cid, "No buttons")
            else:
                for i, b in enumerate(user_buttons):
                    kb = InlineKeyboardMarkup()
                    kb.row(InlineKeyboardButton(f"🗑 Remove {b['name']}", callback_data=f"userbtn_remove_{i}"))
                    bot.send_message(cid, f"🔹 {b['name']} ({b['type']})", reply_markup=kb)
        elif data.startswith("userbtn_remove_"):
            i = int(data.split("_")[-1])
            if i < len(user_buttons):
                user_buttons.pop(i)
                bot.send_message(cid, "🗑 Button removed")
        elif data.startswith("btn_type_"):
            tp = data.split("_")[-1]
            name_data = temp_data.get(cid, {})
            if not name_data or "button_name" not in name_data:
                bot.send_message(cid, "❌ Session expired, start again.")
                return
            temp_data[cid]["type"] = tp
            settings_state[cid] = "awaiting_button_content"
            bot.send_message(cid, f"📤 Send {tp.upper()} for button <b>{name_data['button_name']}</b>")
        elif data == "grouplink_remove":
            group_forward_link = None
            bot.send_message(cid, "🗑 Group link removed")
        elif data == "groupadmin_done":
            link = temp_data.get(cid)
            if not link:
                bot.send_message(cid, "❌ Session expired")
                return
            try:
                chat = bot.get_chat(link)
                member = bot.get_chat_member(link, bot.get_me().id)
                if member.status in ['administrator', 'creator']:
                    group_forward_link = link
                    settings_state.pop(cid, None)
                    temp_data.pop(cid, None)
                    bot.send_message(cid, f"✅ Bot is admin in {link}\nForwarding enabled.", reply_markup=settings_kb)
                else:
                    bot.send_message(cid, "❌ Bot not admin. Make admin and press RETRY.", reply_markup=InlineKeyboardMarkup().row(
                        InlineKeyboardButton("✅ RETRY", callback_data="groupadmin_done"), InlineKeyboardButton("❌ CANCEL", callback_data="groupadmin_cancel")))
            except Exception as e:
                bot.send_message(cid, f"❌ Could not check: {e}\nMake sure username is correct and bot is admin. Press RETRY.", reply_markup=InlineKeyboardMarkup().row(
                    InlineKeyboardButton("✅ RETRY", callback_data="groupadmin_done"), InlineKeyboardButton("❌ CANCEL", callback_data="groupadmin_cancel")))
        elif data == "groupadmin_cancel":
            settings_state.pop(cid, None)
            temp_data.pop(cid, None)
            bot.send_message(cid, "❌ Cancelled", reply_markup=settings_kb)
        elif data == "joinrqd_new":
            settings_state[cid] = "awaiting_join_link"
            bot.send_message(cid, "Send new group/channel username")
        elif data == "joinrqd_remove":
            join_required_link = None; join_required_message = None
            bot.send_message(cid, "🗑 Join requirement removed")
        elif data == "delbot_confirm":
            bot.send_message(cid, "💀 Bot shutting down...")
            bot.stop_polling()
            exit(0)
        elif data == "delbot_cancel":
            bot.send_message(cid, "✅ Cancelled", reply_markup=settings_kb)
    except Exception as e:
        print(f"Callback error: {e}\n{traceback.format_exc()}")

# =========================================================
# COMING SOON
# =========================================================

@bot.message_handler(func=lambda m: m.text == "⚡ Advance Tools")
def advance_tools(message):
    try:
        if message.chat.id != ADMIN_ID: return
        bot.send_message(message.chat.id, "🚀 <b>PREMIUM FEATURE COMING SOON</b>")
    except Exception as e:
        print(f"Advance tools error: {e}")

# =========================================================
# REMOVE WEBHOOK & RUN
# =========================================================
print("🧹 Removing webhook...")
bot.remove_webhook()
time.sleep(1)
print("🔥 PREMIUM BOT RUNNING - ALL FEATURES ACTIVE")
print("▰▰▰▰▰▰▰▰▰▰ 100%")
bot.infinity_polling()
