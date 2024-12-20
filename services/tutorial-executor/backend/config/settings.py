# -*- coding: utf-8 -*-
"""
Settings Configuration

This module contains the configuration settings for the application.
It includes configurations for database connections, API keys, paths,
environment variables, and other necessary settings.
"""

import os
from pathlib import Path
from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict

class Settings(BaseSettings):
    """
    Pydantic model for application settings.

    This class loads environment variables from a `.env` file or from the system's environment.
    """

    # Project infomation
    PROJECT_NAME: str = "Tuturial Executor"
    API_VERSION: str = "1.0"

    # Config path
    CONFIG_PATH: str = "config/demo_mode.toml"
    
    # Application settings
    APP_NAME: str = "My Awesome App"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # MongoDB settings
    MONGODB_URL: AnyUrl = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "mydatabase"

    # API Keys and Secrets
    API_KEY: str = "default_api_key"
    SECRET_KEY: str = "default_secret_key"

    # Email settings
    EMAIL_HOST: str = "smtp.example.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = "user@example.com"
    EMAIL_PASSWORD: str = "password"
    EMAIL_FROM: str = "noreply@example.com"

    # File storage settings
    STORAGE_PATH: Path = Path("/var/app/storage")
    MAX_FILE_SIZE_MB: int = 10

    # Security settings
    JWT_SECRET_KEY: str = "jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"

    # External services
    EXTERNAL_API_BASE_URL: str = "https://api.example.com/v1"
    EXTERNAL_API_TIMEOUT_SECONDS: int = 10

    # Feature flags
    ENABLE_FEATURE_X: bool = True
    ENABLE_FEATURE_Y: bool = False

    # Caching settings
    CACHE_TYPE: str = "simple"  # Options: 'simple', 'redis', 'memcached'
    REDIS_URL: Optional[AnyUrl] = None  # Required if CACHE_TYPE is 'redis'

    # Pagination settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Localization and internationalization (i18n) settings
    SUPPORTED_LANGUAGES: List[str] = ["en", "es", "fr"]
    DEFAULT_LANGUAGE: str = "en"

    # Timezone settings
    TIMEZONE: str = "UTC"

    # Rate limiting settings
    RATE_LIMIT_STR: str = "5/minute"  # Format: "{number_of_requests}/{time_window}"

    # CORS (Cross-Origin Resource Sharing) settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "https://example.com"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["Authorization", "Content-Type"]

    # Social media integrations
    SOCIAL_AUTH_FACEBOOK_KEY: Optional[str] = None
    SOCIAL_AUTH_FACEBOOK_SECRET: Optional[str] = None
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: Optional[str] = None
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: Optional[str] = None

    # Payment gateway integration
    PAYMENT_GATEWAY_API_KEY: Optional[str] = None
    PAYMENT_GATEWAY_SECRET_KEY: Optional[str] = None

    # Analytics and tracking
    GOOGLE_ANALYTICS_ID: Optional[str] = None
    SEGMENT_WRITE_KEY: Optional[str] = None

    # Monitoring and health checks
    HEALTH_CHECK_PATH: str = "/health"
    PROMETHEUS_METRICS_PATH: str = "/metrics"

    # Background tasks and job queues
    CELERY_BROKER_URL: Optional[AnyUrl] = None
    CELERY_RESULT_BACKEND: Optional[AnyUrl] = None

    # Testing settings
    TEST_MONGODB_URI: AnyUrl = "mongodb://localhost:27017/testdb"

    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Initialize settings
settings = Settings()

if __name__ == '__main__':
    print("Application Name:", settings.APP_NAME)
    print("MongoDB URI:", settings.MONGODB_URI)
    print("API Key:", settings.API_KEY)

    # Print additional settings to demonstrate usage
    print("Supported Languages:", settings.SUPPORTED_LANGUAGES)
    print("Default Language:", settings.DEFAULT_LANGUAGE)
    print("Timezone:", settings.TIMEZONE)
    print("Rate Limit:", settings.RATE_LIMIT_STR)
    print("CORS Origins:", settings.CORS_ORIGINS)