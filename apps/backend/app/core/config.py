"""
Application Configuration
Settings management using Pydantic BaseSettings
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # Project Info
    PROJECT_NAME: str = "CareerNavigator API"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://cnav:dev_password@localhost:5432/careernavigator",
        description="PostgreSQL database URL",
    )

    # Neo4j
    NEO4J_URI: str = Field(
        default="bolt://localhost:7687",
        description="Neo4j connection URI",
    )
    NEO4J_USER: str = Field(default="neo4j", description="Neo4j username")
    NEO4J_PASSWORD: str = Field(
        default="dev_password", description="Neo4j password"
    )

    # Qdrant
    QDRANT_URL: str = Field(
        default="http://localhost:6333", description="Qdrant URL"
    )

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379", description="Redis URL"
    )

    # LLM APIs
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None, description="Anthropic API key"
    )
    COHERE_API_KEY: Optional[str] = Field(default=None, description="Cohere API key")

    # External APIs
    INDEED_API_KEY: Optional[str] = Field(default=None, description="Indeed API key")
    WORKNET_API_KEY: Optional[str] = Field(default=None, description="WorkNet API key")

    # Auth
    JWT_SECRET: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT secret key",
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, description="Access token expiration in minutes"
    )

    # Azure (Production)
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = Field(
        default=None, description="Azure Storage connection string"
    )
    AZURE_APPLICATION_INSIGHTS_KEY: Optional[str] = Field(
        default=None, description="Azure Application Insights key"
    )

    # Monitoring
    LANGSMITH_API_KEY: Optional[str] = Field(
        default=None, description="LangSmith API key"
    )
    LANGSMITH_PROJECT: str = Field(
        default="careernavigator-dev", description="LangSmith project name"
    )
    SENTRY_DSN: Optional[str] = Field(default=None, description="Sentry DSN")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
