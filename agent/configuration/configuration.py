from pathlib import Path

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

# Настройка конфигурации из файла .env и валидация имен переменных окружения
class Config(BaseSettings):
    gigachat_credentials: str = Field(validation_alias="GIGACHAT_CREDENTIALS")
    gigachat_scope: str = Field(validation_alias="GIGACHAT_SCOPE")
    gigachat_temperature: float = Field(validation_alias="GIGACHAT_TEMPERATURE")
    gigachat_verify_ssl: bool = Field(validation_alias="GIGACHAT_VERIFY_SSL")

    tavily_key: str = Field(validation_alias="TAVILY_API_KEY")

    project_root: Path = Path(__file__).resolve().parents[2]
    env_file_path: Path = project_root / ".env"

    if env_file_path.is_file():
        model_config = SettingsConfigDict(env_file=env_file_path, extra="ignore", validate_default=False)
    

configuration = Config()