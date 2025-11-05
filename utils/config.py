import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")
    admin_ids: str = Field(default="", alias="ADMIN_IDS")
    
    virustotal_api_key: Optional[str] = Field(None, alias="VIRUSTOTAL_API_KEY")
    abuseipdb_api_key: Optional[str] = Field(None, alias="ABUSEIPDB_API_KEY")
    hibp_api_key: Optional[str] = Field(None, alias="HIBP_API_KEY")
    
    jnetrack_api_key: Optional[str] = Field(None, alias="JNETRACK_API_KEY")
    jnttrack_api_key: Optional[str] = Field(None, alias="JNTTRACK_API_KEY")
    sicepat_api_key: Optional[str] = Field(None, alias="SICEPAT_API_KEY")
    
    rate_limit_requests: int = Field(10, alias="RATE_LIMIT_REQUESTS")
    rate_limit_period: int = Field(60, alias="RATE_LIMIT_PERIOD")
    
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    log_file: str = Field("logs/bot.log", alias="LOG_FILE")
    audit_log_file: str = Field("logs/audit.log", alias="AUDIT_LOG_FILE")
    
    redis_host: str = Field("localhost", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_db: int = Field(0, alias="REDIS_DB")
    redis_password: Optional[str] = Field(None, alias="REDIS_PASSWORD")
    
    allowed_chat_types: str = Field(default="private,group", alias="ALLOWED_CHAT_TYPES")
    require_whitelist: bool = Field(False, alias="REQUIRE_WHITELIST")
    whitelist_users: str = Field(default="", alias="WHITELIST_USERS")
    
    def get_admin_ids(self) -> List[int]:
        if not self.admin_ids.strip():
            return []
        return [int(x.strip()) for x in self.admin_ids.split(',') if x.strip()]
    
    def get_whitelist_users(self) -> List[int]:
        if not self.whitelist_users.strip():
            return []
        return [int(x.strip()) for x in self.whitelist_users.split(',') if x.strip()]
    
    def get_allowed_chat_types(self) -> List[str]:
        if not self.allowed_chat_types.strip():
            return ["private", "group"]
        return [x.strip() for x in self.allowed_chat_types.split(',') if x.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


_settings = Settings()

class SettingsProxy:
    def __init__(self, base_settings):
        self._settings = base_settings
        self.admin_ids = base_settings.get_admin_ids()
        self.whitelist_users = base_settings.get_whitelist_users()
        self.allowed_chat_types = base_settings.get_allowed_chat_types()
    
    def __getattr__(self, name):
        return getattr(self._settings, name)

settings = SettingsProxy(_settings)
