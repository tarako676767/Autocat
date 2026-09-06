import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

# --- Flask Server (Keep-alive) ---
app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run():
    # Render等のポート指定に対応
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord Bot ---
load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

STATUS = "❤にゃんこ大戦争自動代行❤"

async def load_cogs():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

bot.setup_hook = load_cogs

@bot.event
async def on_ready():
    print("🤖 Bot Is Ready.")
    await bot.change_presence(activity=discord.Game(name=STATUS), status=discord.Status.idle)
    
    # スラッシュコマンドの全同期処理
    try:
        synced = await bot.tree.sync()
        print(f"✅ 全コマンド ({len(synced)}個) の同期が完了しました。")
    except Exception as e:
        print(f"❌ 同期エラー: {e}")

if __name__ == "__main__":
    # Flaskサーバーを別スレッドで起動
    keep_alive()
    
    # Botの起動
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ TOKENが見つかりません。")
