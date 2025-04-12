from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Email settings
    EMAIL_SERVER: str = "imap.gmail.com"
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    
    # Flask settings
    FLASK_SECRET_KEY: str = "your-secret-key-here"
    
    # WhatsApp settings (using Telegram Bot API as an example)
    TELEGRAM_BOT_TOKEN: str = ""
    
    # Service groups
    SERVICE_GROUPS: List[str] = [
        "Technical Support",
        "Billing",
        "Account Management",
        "General Inquiry"
    ]
    
    # Model settings
    CLASSIFICATION_MODEL: str = "distilbert-base-uncased"
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings() 