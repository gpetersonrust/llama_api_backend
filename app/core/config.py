import os
from dotenv import load_dotenv

load_dotenv()  ## load environment variables from .env file


class Settings:  ## Settings class to hold configuration values
    ALLOWED_ORIGIN = os.getenv(
        "ALLOWED_ORIGIN", "http://chatbot-python-2025.local"
    )  ## Allowed origin for CORS
    LLAMA_MODEL = os.getenv("LLAMA_MODEL", "llama3.1:8b")  ## LLaMA model name
    ALLOWED_METHODS = ["POST"]  ## Allowed HTTP methods


settings = Settings()
