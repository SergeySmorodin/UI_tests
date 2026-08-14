from playwright.sync_api import Page
import os
from datetime import datetime


class DebugMixin:
    """Миксин для отладки"""

    page: Page

    def take_screenshot(self, name: str = "screenshot", full_page: bool = True):
        """
        Сделать скриншот страницы

        Args:
            name: Имя файла скриншота (без расширения)
            full_page: Делать ли скриншот всей страницы

        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем папку для скриншотов, если её нет
        os.makedirs("screenshots", exist_ok=True)

        # Добавляем временную метку к имени файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"

        try:
            self.page.screenshot(path=filename, full_page=full_page)
            print(f"✓ Скриншот сохранен: {filename}")
            return filename
        except Exception as e:
            print(f"✗ Ошибка при создании скриншота: {e}")
            raise

    def save_page_content(self, name: str = "page_content", add_info: bool = True, pretty_print: bool = True):
        """
        Сохранить HTML контент страницы для анализа

        Args:
            name: Имя файла (без расширения)
            add_info: Добавлять ли служебную информацию в начало файла
            pretty_print: Форматировать ли HTML с отступами

        Returns:
            str: Путь к сохраненному файлу
        """
        # Создаем папку для сохранения, если её нет
        os.makedirs("debug", exist_ok=True)

        # Добавляем временную метку к имени файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"debug/{name}_{timestamp}.html"

        # Получаем HTML контент страницы
        page_content = self.page.content()

        if pretty_print:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(page_content, 'html.parser')
                page_content = soup.prettify()
            except ImportError:
                print("⚠ BeautifulSoup не установлен. Используйте: pip install beautifulsoup4")
                print("Сохраняем без форматирования...")
                page_content = self._simple_html_format(page_content)

        if add_info:
            # Добавляем служебную информацию в начало файла
            info = f"""<!-- 
                URL: {self.page.url}
                Title: {self.page.title()}
                Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                Page Class: {self.__class__.__name__}
                -->
                """
            page_content = info + page_content

        # Сохраняем HTML в файл
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page_content)

        print(f"✓ HTML страницы сохранен: {filename}")

        # Также сохраняем копию с фиксированным именем для быстрого доступа
        fixed_filename = f"debug/{name}_latest.html"
        with open(fixed_filename, "w", encoding="utf-8") as f:
            f.write(page_content)
        print(f"✓ HTML страницы сохранен: {fixed_filename}")

        return filename

    def save_page_source(self, name: str = "page_source"):
        """
        Сохранить исходный код страницы (аналог save_page_content)

        Args:
            name: Имя файла (без расширения)

        Returns:
            str: Путь к сохраненному файлу
        """
        return self.save_page_content(name)

    def debug_info(self, save_html: bool = False, save_screenshot: bool = False):
        """
        Вывести отладочную информацию о странице

        Args:
            save_html: Сохранять ли HTML контент
            save_screenshot: Сохранять ли скриншот
        """
        print(f"\n=== DEBUG: {self.__class__.__name__} ===")
        print(f"URL: {self.page.url}")
        print(f"Title: {self.page.title()}")

        if save_html:
            self.save_page_content()

        if save_screenshot:
            self.take_screenshot()

        print("=== END DEBUG ===\n")

    def save_debug_artifacts(self, prefix: str = "debug"):
        """
        Сохранить все отладочные артефакты (HTML + скриншот)

        Args:
            prefix: Префикс для имен файлов

        Returns:
            dict: Словарь с путями к сохраненным файлам
        """
        artifacts = {}

        # Сохраняем HTML
        html_path = self.save_page_content(f"{prefix}_page")
        artifacts['html'] = html_path

        # Сохраняем скриншот
        screenshot_path = self.take_screenshot(f"{prefix}_screenshot")
        artifacts['screenshot'] = screenshot_path

        print(f"\n=== Сохраненные артефакты ===")
        for key, value in artifacts.items():
            print(f"{key}: {value}")

        return artifacts

    def _simple_html_format(self, html_content: str) -> str:
        """
        Простое форматирование HTML без BeautifulSoup

        Args:
            html_content: HTML контент

        Returns:
            str: Отформатированный HTML
        """
        # Добавляем переносы строк после тегов
        formatted = html_content.replace('><', '>\n<')

        # Добавляем отступы
        lines = formatted.split('\n')
        indented_lines = []
        indent_level = 0

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Уменьшаем отступ для закрывающих тегов
            if line.startswith('</'):
                indent_level = max(0, indent_level - 1)

            # Добавляем отступ
            indented_lines.append('  ' * indent_level + line)

            # Увеличиваем отступ для открывающих тегов
            if (line.startswith('<') and
                    not line.startswith('</') and
                    not line.startswith('<!') and
                    not line.endswith('/>') and
                    not line.startswith('<meta') and
                    not line.startswith('<link') and
                    not line.startswith('<input')):
                indent_level += 1

        return '\n'.join(indented_lines)
