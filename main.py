import discord
from discord.ext import commands
import os
import threading
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
owner_id_env = os.getenv('OWNER_ID',1399633592681889864)
owner_id = int(owner_id_env) if owner_id_env else None

# --- Flaskの設定 ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.getenv("PORT", 10000))
    # ログ出力で停止しないよう処理
    app.run(host='0.0.0.0', port=port, use_reloader=False)

# Flaskを非同期スレッドで先に起動
t = threading.Thread(target=run_flask, daemon=True)
t.start()

# --- Discord Botの設定 ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None, owner_id=owner_id)

async def load_cogs():
    print("🔄 --- Cogの読み込みを開始します ---")
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
                print(f"✅ Loaded: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")
                
    print("🔄 --- コマンドの同期(sync)を実行中... ---")
    try:
        synced = await bot.tree.sync()
        print(f"✅ 全 {len(synced)} 件のコマンドを同期しました！")
    except Exception as e:
        print(f"❌ Sync失敗: {e}")

bot.setup_hook = load_cogs

STATUS = "❤にゃんこ大戦争自動代行❤"

@bot.event
async def on_ready():
    print(f"🤖 Botが正常に起動しました: {bot.user}")
    await bot.change_presence(activity=discord.Game(name=STATUS), status=discord.Status.idle)

if __name__ == "__main__":
    if token:
        bot.run(token)
    else:
        print("❌ エラー: 環境変数 TOKEN が設定されていません。")
