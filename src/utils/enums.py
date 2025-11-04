"""
Clappia MCP Enums

This module contains all enum definitions used across the Clappia MCP server.
"""

from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    QA = "qa"
    PROD = "prod"

    @classmethod
    def from_string(cls, value: str) -> "Environment":
        value_lower = value.lower().strip()
        try:
            return cls(value_lower)
        except ValueError:
            raise ValueError(
                f"Invalid ENVIRONMENT value: {value}. Must be one of: {', '.join([e.value for e in cls])}"
            )

    @classmethod
    def from_env(
        cls, env_var: str = "ENVIRONMENT", default: "Environment" = None
    ) -> "Environment":
        import os

        env_value = os.getenv(env_var, default.value if default else cls.DEV.value)
        return cls.from_string(env_value)

    def is_production(self) -> bool:
        return self == Environment.PROD
