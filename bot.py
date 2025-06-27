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
    "🎬 Episode 1": "https://worker-holy-term-114f.xijofa2769.workers.dev/5b66ece097753c4134a7514297d4ca289d3f34052cefb7642cd918631e759893de8743e50008e413eec61e5df61cf489a7f29713f42480f728a7ed6690bb8b2de270aea0f879cc6af9e188034171e77f45695447ada796cf0b428920ba7e6ceac539e150a371e413a79e6889eadcba6721744c7c6ff995f8ea08b9889dfa1f253da18880592ca2be96952feb4cb45d22b982cc4b28b4f4d02188aad564563f6363497c2c6a7c9a49c984707fde1cd89a::f671fe70b2daa4d11bd2a0041944450e/Squid%20Game%20S03E01%202160p%20NF%20WEBDL%20DV%20HDR%2010bit%20HEVC%20[Hindi%20DDP%205.1%20%20EnglishKorean%20DDP%205.1]%20x265%20(HHWEBUHDMovies).mkv",
    "🎬 Episode 2": "https://worker-weathered-king-dfe2.pexovav401.workers.dev/cba508331113d9777b9d6425efe6f86d726b4a82b7a292910b131e0e036f5bf4d6640847dbdf88549c5690bc5c9fdd36db91770b8e269dcaef547be523bac8a694feb63d397864a220b7d6e6c6f3ffb2471ea61e1e49d47de9024800d8a34eddbc1c7e68da62ab9e4fd7df5121558953d528943b0c8477028fdbd18fdf317d8c9024dcc61d7df7cf39fc220922ca4576d80a1a279d58070bf7b4f9f1942f6a9ed8fe2269228a8cabcdab05911e6b6853::8fb076df40040f5a4aca760623950bfb/Squid%20Game%20S03E02%202160p%20NF%20WEBDL%20DV%20HDR%2010bit%20HEVC%20[Hindi%20DDP%205.1%20%20EnglishKorean%20DDP%205.1]%20x265%20(HHWEBUHDMovies).mkv",
    "🎬 Episode 3": "https://worker-old-thunder-81dd.laweco7721.workers.dev/2796cd2e1ca28be791290ac4a591815bebe4c713051b6e716815aae65a5e2e0965b6739d589622b32807bad07d9aa9a3b3507e168384b6ef454f1868bfe55c835873e620815e1046d34587691e6defb89b15e57400844e9b8e889b84add2915cabc72d0d4d48a8491d97a068ead3cc1918595356ab3acbb2a16c8e4358b166a842bc3634de11e4a1d19e6aacae93386608b40eb0230a4322b8f44b5f47b7188b9dbee17e55104c39a16710b2c6accb0e::59c754c7071aa491cf529e988a7f68c3/Squid%20Game%20S03E03%202160p%20NF%20WEBDL%20DV%20HDR%2010bit%20HEVC%20[Hindi%20DDP%205.1%20%20EnglishKorean%20DDP%205.1]%20x265%20(HHWEBUHDMovies).mkv",
    "🎬 Episode 4": "https://worker-empty-math-b0f8.cekiv18910.workers.dev/88033f66612fd78bb050677fa0e959aa706a6d54aec273531e1589f8dd3d0ba6ed6dab82139857b7e336747cca832e22bdb1c9b464872e657da57223b64dba455d0afcaf22455bab66d7add76b0929b4fa9539ee91ec69728eb3b2ff436392db9fdfa5a85790a671acfeb67215cbc5630ef63acaaffed9e46684c649d0b05f01d034c4d9a31233f31659a4fa539de9355686505ec54570714a6fd8ce47de3d992adb9eec59ffad33bcbb0e658f2adaad::3f03d9a0a8285b94adb81050613a8853/Squid%20Game%20S03E04%202160p%20NF%20WEBDL%20DV%20HDR%2010bit%20HEVC%20[Hindi%20DDP%205.1%20%20EnglishKorean%20DDP%205.1]%20x265%20(HHWEBUHDMovies).mkv",
    "🎬 Episode 5": "https://worker-red-silence-1f45.tefika4630.workers.dev/6314c485657b91be1b39dfdd48e6a284b266757b64a0e9fe191c0fa55cc180dd08a173bcc2219b28c2e27d7719af8113740e155e68ce5250c94a2cc6be9b2f204fdaef7fa93548494a3885e7a7a37f63b77e268a3b545f4ae3c550d3e8daab73eef955f6820088f45c1ccd741d6045c652cad93787441129720952fe40f741d79439570401f22723d2d9234cbedc205390446b8d8b624177434626b0129fd8f9b6981863b597e5dcae5ecf4db146e423::c0f7d1409c1ca9e1a95f5d38b690deb2/Squid%20Game%20S03E05%202160p%20NF%20WEBDL%20DV%20HDR%2010bit%20HEVC%20[Hindi%20DDP%205.1%20%20EnglishKorean%20DDP%205.1]%20x265%20(HHWEBUHDMovies).mkv",
    "🎬 Episode 6": "https://worker-frosty-bread-8050.moloyok562.workers.dev/bf88a212a048178e5cd1fdca9121dccc88773e485a660d0e637720b46123be0cce85b7a24fb4eeccd7b9be46e3d4979488f834a9d0bf9bad343c93d6cb03ad4e195d7e3cc082b6d0dd88f3256960dec203fa9901bb8a79f58ebccef50fc8b3c08666e264ff539b6de08bd1bbdd3b015875796011a01bc5e72db75c0c8e8af71aad03b069f2317d94184fba90d01d710bb61e3e309b34f49cbbde70d1e9254f6cff39b38502834b4d5d79c8f7af2e240e::b4612c5b42895258939258f2c16e20c2/Squid%20Game%20S03E06%202160p%20NF%20WEBDL%20DV%20HDR%2010bit%20HEVC%20[Hindi%20DDP%205.1%20%20EnglishKorean%20DDP%205.1]%20x265%20(HHWEBUHDMovies).mkv"
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
