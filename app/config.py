import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MASTER_ID = os.getenv("MASTER_ID")
if not BOT_TOKEN or not MASTER_ID:
    raise ValueError("BOT_TOKEN and MASTER_ID must be set in environment")
try:
    MASTER_ID = int(MASTER_ID)
except ValueError:
    raise ValueError("MASTER_ID must be an integer")

PORTFOLIO_URL = os.getenv("PORTFOLIO_URL", "").strip()
REVIEWS_URL = os.getenv("REVIEWS_URL", "").strip()
SKETCHES_URL = os.getenv("SKETCHES_URL", "").strip()

# Flag to enable/disable receiving new leads (can be toggled via /admin)
RECEIVE_LEADS = True
