import discord
from discord.ext import commands
from discord import app_commands
import os
import traceback
import threading
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
owner_id = int(os.getenv('OWNER_ID', 1399633592681889864))

# --- Render/Flask 設定 (Keep-alive) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Renderから割り当てられるPORTを取得（デフォルトは10000）
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- Discord Bot 設定 ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None, owner_id=owner_id)

async def load_cogs():
    for filename in os.listdir("./Cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"Cogs.{filename[:-3]}")
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")
    await bot.tree.sync()
    print("✅ Commands synced")

bot.setup_hook = load_cogs

STATUS = "❤にゃんこ大戦争自動代行❤"

@bot.event
async def on_ready():
    print("🤖 Bot Is Ready.")
    await bot.change_presence(activity=discord.Game(name=STATUS), status=discord.Status.idle)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        print(f"❌ {interaction.user}によるコマンド({interaction.command.name})の実行がブロックされました。")
        return
    print(f"❌ Error: {error}")
    traceback.print_exc()

if __name__ == "__main__":
    # Webサーバー起動
    keep_alive()
    
    # Bot起動
    bot.run(token)
