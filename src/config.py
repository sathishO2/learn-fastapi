# from pydantic_settings import BaseSettings, SettingsConfigDict

# class Settings(BaseSettings):
#     DATABASE_URL: str

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore",
#     )


# # inside src/config.py
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     DATABASE_URL: str 

#     model_config = SettingsConfigDict(
#         env_file=".env", 
#         extra="ignore"
#     )

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()  # Manually load .env file

class Settings(BaseSettings):
    DATABASE_URL: str 

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

Config = Settings()
