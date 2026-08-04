# config.py
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

# Загружаем .env файл
load_dotenv()


@dataclass
class VPNConfig:
    """Конфигурация VPN и тестовых данных"""
    site_url: str
    login: str
    password: str
    dashboard_url: Optional[str] = None
    timeout: int = 30000
    headless: bool = False

    @classmethod
    def from_env(cls) -> 'VPNConfig':
        """Создание конфигурации из переменных окружения"""
        # Преобразование строки в булево значение
        headless_str = os.getenv('BROWSER_HEADLESS', 'false').lower()
        headless = headless_str in ('true', '1', 'yes')

        print(f"\n📋 Конфигурация загружена:")
        print(f"   BROWSER_HEADLESS из .env: '{os.getenv('BROWSER_HEADLESS')}'")
        print(f"   Преобразовано в: {headless}")
        print(f"   Сайт: {os.getenv('VPN_SITE_URL')}")
        print(f"   Логин: {os.getenv('VPN_LOGIN')}")

        return cls(
            site_url=os.getenv('SITE_URL', 'https://172.16.226.34/'),
            login=os.getenv('LOGIN', ''),
            password=os.getenv('PASSWORD', ''),
            timeout=int(os.getenv('DEFAULT_TIMEOUT', '30000')),
            headless=headless
        )


# Глобальный экземпляр конфигурации
vpn_config = VPNConfig.from_env()
