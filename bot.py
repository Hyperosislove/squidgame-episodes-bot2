from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Bot Token
TOKEN = "8043507297:AAGyWv9WwfR_qNvrgwioXUzgdYTdz9A1XDo"

# Your Channel Username (without @)
CHANNEL_USERNAME = "squidgame3allepisodes"

# Squid Game Episode Links
episode_links = {
    "🎬 Episode 1": "https://worker-holy-term-114f.xijofa2769.workers.dev/...",
    "🎬 Episode 2": "https://worker-weathered-king-dfe2.pexovav401.workers.dev/...",
    "🎬 Episode 3": "https://worker-old-thunder-81dd.laweco7721.workers.dev/...",
    "🎬 Episode 4": "https://worker-empty-math-b0f8.cekiv18910.workers.dev/...",
    "🎬 Episode 5": "https://worker-red-silence-1f45.tefika4630.workers.dev/...",
    "🎬 Episode 6": "https://worker-frosty-bread-8050.moloyok562.workers.dev/..."
}

# Logging (for Heroku logs)
logging.basicConfig(level=logging.INFO)

# Function to check if user is subscribed
async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = user.id

    if not await check_subscription(chat_id, context):
        keyboard = [
            [InlineKeyboardButton("📢 Join Now", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="joined")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"""👋 **Welcome, {user.first_name}!**

🔥 You're just one step away from watching **Squid Game Season 3** in stunning **4K Ultra HD** quality with **Hindi + English + Korean audio**.  
👉 To unlock all episodes, please join our official channel first:

🔒 **This helps us keep the content free for everyone!**

👇 Click below to join and then tap “I’ve Joined”
""",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    await send_episode_buttons(update, context)

# Send Episode Buttons
async def send_episode_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(ep, url=link)] for ep, link in episode_links.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "**✅ Access Granted!**\n\nChoose an episode below and enjoy the show 🍿:\n\n📺 _Streaming in 4K Dolby Vision_ 🔊",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Callback from "I’ve Joined"
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if not await check_subscription(user_id, context):
        await query.edit_message_text(
            "❌ You haven't joined the channel yet.\n\nPlease join first to unlock the episodes:\n👉 https://t.me/" + CHANNEL_USERNAME
        )
        return

    # User joined successfully
    keyboard = [[InlineKeyboardButton(ep, url=link)] for ep, link in episode_links.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "**✅ Access Granted!**\n\nChoose an episode below and enjoy the show 🍿:\n\n📺 _Streaming in 4K Dolby Vision_ 🔊",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Initialize App
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))

# Run
app.run_polling()
