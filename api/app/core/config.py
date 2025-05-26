import os
from typing import List, Optional
from pydantic_settings import BaseSettings
import json


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Staff Platform"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = "fallback-secret-key-change-in-production"
    
    # Database
    database_url: str = "sqlite:///./ai_staff_platform.db"
    
    # AI Configuration (Optional for demo)
    openai_api_key: Optional[str] = None
    langchain_api_key: Optional[str] = None
    langchain_tracing_v2: bool = False
    langchain_project: str = "ai-staff-platform"
    
    # Security
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    
    # CORS - parse from environment variable
    backend_cors_origins: List[str] = ["*"]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins from environment if set as JSON string
        cors_env = os.getenv('BACKEND_CORS_ORIGINS')
        if cors_env:
            try:
                self.backend_cors_origins = json.loads(cors_env)
            except:
                self.backend_cors_origins = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
