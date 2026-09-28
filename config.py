from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    SECRET_KEY:str
    EXPIRATION_TIME:int
    ALGORITHM:str
    URL:str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings=Settings()