from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Bot token and channel
TOKEN = "8043507297:AAGyWv9WwfR_qNvrgwioXUzgdYTdz9A1XDo"
CHANNEL_USERNAME = "squidgame3allepisodes"

# List of users who already clicked "I've Joined"
joined_users = set()

# Episode links
episode_links = {
    "🎬 Episode 1": "https://worker-holy-term-114f.xijofa2769.workers.dev/...",
    "🎬 Episode 2": "https://worker-weathered-king-dfe2.pexovav401.workers.dev/...",
    "🎬 Episode 3": "https://worker-old-thunder-81dd.laweco7721.workers.dev/...",
    "🎬 Episode 4": "https://worker-empty-math-b0f8.cekiv18910.workers.dev/...",
    "🎬 Episode 5": "https://worker-red-silence-1f45.tefika4630.workers.dev/...",
    "🎬 Episode 6": "https://worker-frosty-bread-8050.moloyok562.workers.dev/..."
}

logging.basicConfig(level=logging.INFO)

# Show episode buttons
async def send_episode_buttons(chat_id, context):
    keyboard = [[InlineKeyboardButton(ep, url=link)] for ep, link in episode_links.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="**✅ Access Granted!**\n\nChoose an episode below and enjoy the show 🍿:\n\n📺 _Streaming in 4K Dolby Vision_ 🔊",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = user.id

    if chat_id in joined_users:
        await send_episode_buttons(chat_id, context)
        return

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("✅ I’ve Joined", callback_data="joined")]
    ]
    await update.message.reply_text(
        f"""👋 **Welcome, {user.first_name}!**

🔥 You're just one step away from watching **Squid Game Season 3** in 4K Ultra HD with Hindi, English & Korean audio.

Please join the channel to unlock all episodes 🔓

👇 Tap below to join, then press “I’ve Joined”
""",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Button callback
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "joined":
        joined_users.add(user_id)
        await query.edit_message_text("✅ Access Granted! Please select an episode below.")
        await send_episode_buttons(user_id, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

app.run_polling()
