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
        return cls(
            site_url=os.getenv('VPN_SITE_URL', 'https://172.16.226.34/login'),
            login=os.getenv('VPN_LOGIN', ''),
            password=os.getenv('VPN_PASSWORD', ''),
            dashboard_url=os.getenv('VPN_DASHBOARD_URL'),
            timeout=int(os.getenv('DEFAULT_TIMEOUT', '30000')),
            headless=os.getenv('BROWSER_HEADLESS', 'false').lower() == 'true'
        )


# Создаем глобальный экземпляр конфигурации
vpn_config = VPNConfig.from_env()

# Для обратной совместимости (если нужны отдельные переменные)
VPN_SITE_URL = vpn_config.site_url
VPN_LOGIN = vpn_config.login
VPN_PASSWORD = vpn_config.password