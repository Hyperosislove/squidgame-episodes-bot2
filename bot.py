from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import aiohttp

# Telegram Bot Token
TOKEN = "8043507297:AAGyWv9WwfR_qNvrgwioXUzgdYTdz9A1XDo"

# Channel username for force subscription (without @)
CHANNEL_USERNAME = "squidgame3allepisodes"

# Episode links
episode_links = {
    "Episode 1": "https://worker-holy-term-114f.xijofa2769.workers.dev/...",
    "Episode 2": "https://worker-weathered-king-dfe2.pexovav401.workers.dev/...",
    "Episode 3": "https://worker-old-thunder-81dd.laweco7721.workers.dev/...",
    "Episode 4": "https://worker-empty-math-b0f8.cekiv18910.workers.dev/...",
    "Episode 5": "https://worker-red-silence-1f45.tefika4630.workers.dev/...",
    "Episode 6": "https://worker-frosty-bread-8050.moloyok562.workers.dev/..."
}

async def check_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await check_membership(user_id, context):
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🚫 Pehle channel join karo tabhi episodes milenge:", reply_markup=reply_markup)
        return

    # Send episode buttons
    keyboard = [[InlineKeyboardButton(ep, callback_data=ep)] for ep in episode_links]
    await update.message.reply_text("🎬 Select an episode:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if not await check_membership(user_id, context):
        await query.edit_message_text("❌ Pehle channel join karo: https://t.me/" + CHANNEL_USERNAME)
        return

    episode = query.data
    link = episode_links.get(episode, "Link not found.")
    await query.edit_message_text(f"✅ {episode} Link:\n{link}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
