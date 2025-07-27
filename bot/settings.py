from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    bot_token = os.environ.get("BOT_TOKEN", "")
    developer_id = int(os.environ.get("DEVELOPER_ID", 0))


se = Settings()
