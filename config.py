import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Загружаем .env файл
load_dotenv()


@dataclass
class VPNConfig:
    """Конфигурация VPN и тестовых данных"""
    site_url: str
    login: str
    password: str
    timeout: int = 30000
    headless: bool = False

    @classmethod
    def from_env(cls) -> 'VPNConfig':
        """Создание конфигурации из переменных окружения"""
        # Преобразование строки в булево значение
        headless_str = os.getenv('BROWSER_HEADLESS', 'false').lower()
        headless = headless_str in ('true', '1', 'yes')

        return cls(
            site_url=os.getenv('SITE_URL', 'https://172.16.226.34/'),
            login=os.getenv('LOGIN', ''),
            password=os.getenv('PASSWORD', ''),
            timeout=int(os.getenv('DEFAULT_TIMEOUT', '30000')),
            headless=headless
        )


# Глобальный экземпляр конфигурации
vpn_config = VPNConfig.from_env()
