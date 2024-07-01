from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.notification.console_notification import ConsoleNotificationStrategy
from app.notification.sms_notification import SMSNotificationStrategy
from app.storage.json_strategy import JSONStorageStrategy
from app.storage.sql_strategy import SQLStorageStrategy
from .models import Settings
from .scraper import Scraper
from .settings import NOTIFICATION_TYPE, STATIC_TOKEN, DATABASE_FILE, STORAGE_TYPE

app = FastAPI()

security = HTTPBearer()

# Dependency to check the provided token
def get_token_header(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != STATIC_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")
    return credentials.credentials

# Endpoint to start the scraping process
@app.post("/scrape", dependencies=[Depends(get_token_header)])
def scrape_data(settings: Settings):
    if STORAGE_TYPE  == "json":
        storage_strategy = JSONStorageStrategy(DATABASE_FILE)
    elif STORAGE_TYPE == "sql":
        storage_strategy = SQLStorageStrategy("sqlite:///products.db")
    else:
        raise HTTPException(status_code=400, detail="Invalid storage type")
    if NOTIFICATION_TYPE  == "console":
        notification_strategy = ConsoleNotificationStrategy()
    elif NOTIFICATION_TYPE == "sms":
        notification_strategy = SMSNotificationStrategy()
    else:
        raise HTTPException(status_code=400, detail="Invalid notification type")

    scraper = Scraper(settings, storage_strategy,notification_strategy)
    scraper.scrape()
    count = scraper.cache_and_store_results()
    return {"message": f"Scraped and updated {count} products."}
