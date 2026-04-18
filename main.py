import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

# بياناتك اللي استخدمناها قبل كده
api_id = 30600795 
api_hash = "d11ae5d1fc60f17470b72546411175f1"
OWNER_ID = 8583567490 

app = Client("music_session", api_id=api_id, api_hash=api_hash)
call_py = PyTgCalls(app)

@app.on_message(filters.command("vplay", prefixes=".") & filters.user(OWNER_ID))
async def voice_play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ اكتب اسم الأغنية.. مثال: `.vplay تامر حسني` ")
    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 جاري البحث والتشغيل...")
    try:
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
        await call_py.play(message.chat.id, AudioPiped(url))
        await m.edit(f"🎶 **شغال دلوقتي:**\n✅ {info['title']}")
    except Exception as e:
        await m.edit(f"❌ خطأ: {e}")

async def start_bot():
    await app.start()
    await call_py.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
  
