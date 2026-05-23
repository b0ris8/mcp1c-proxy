"""Конфигурация MCP-прокси сервера."""

import sys
from typing import Optional, Literal
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


# === базовая директория (exe-safe) ===
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parents[2]


# дефолтный конфиг рядом с exe / проектом
DEFAULT_CONF_FILE = BASE_DIR / "mcp1c.conf"


class Config(BaseSettings):
    """Настройки MCP-прокси сервера."""

    # === server ===
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000)

    # === 1C ===
    onec_url: str = Field(...)
    onec_username: str = Field(...)
    onec_password: str = Field(...)
    onec_service_root: str = Field(default="mcp")

    # === MCP ===
    server_name: str = Field(default="1C Configuration Data Tools")
    server_version: str = Field(default="1.0.0")

    # === logging ===
    log_level: str = Field(default="INFO")

    # === security ===
    cors_origins: list[str] = Field(default=["*"])

    # === auth ===
    auth_mode: Literal["none", "oauth2"] = Field(default="none")
    public_url: Optional[str] = Field(default=None)
    oauth2_code_ttl: int = Field(default=120)
    oauth2_access_ttl: int = Field(default=3600)
    oauth2_refresh_ttl: int = Field(default=1209600)

    class Config:
        env_prefix = "MCP_"


def get_config(config_path: str | None = None) -> Config:
    """
    Загружает конфиг:
    - если передан путь → используем его
    - иначе → mcp1c.conf рядом с exe
    - env (MCP_*) всегда имеет приоритет над дефолтом
    """

    path = Path(config_path) if config_path else DEFAULT_CONF_FILE

    return Config(_env_file=path)