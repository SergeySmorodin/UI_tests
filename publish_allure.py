#!/usr/bin/env python3

import os
import subprocess
import json
import sys
from datetime import datetime
from pathlib import Path
import shutil


class AllurePublisher:
    def __init__(self, repo_url, results_dir="allure-results",
                 report_dir="allure-report", history_dir="allure-history"):
        self.repo_url = repo_url
        self.results_dir = Path(results_dir)
        self.report_dir = Path(report_dir)
        self.history_dir = Path(history_dir)
        self.build_number = datetime.now().strftime("%Y%m%d-%H%M%S")

    def run_tests(self):
        """Запуск тестов"""
        print("🚀 Запуск тестов...")
        result = subprocess.run(
            ["poetry", "run", "pytest", f"--alluredir={self.results_dir}", "-v"],
            shell=True  # Важно для Windows
        )
        return result.returncode

    def generate_report(self):
        """Генерация Allure отчета"""
        print("📊 Генерация отчета Allure...")

        # Копируем историю если есть
        latest = self.history_dir / "latest"
        if latest.exists() and latest.is_dir():
            history_src = latest / "history"
            if history_src.exists():
                history_dst = self.results_dir / "history"
                history_dst.mkdir(exist_ok=True)
                for f in history_src.glob("*"):
                    if f.is_file():
                        shutil.copy2(f, history_dst)
                print("📂 История скопирована из предыдущего запуска")

        # Генерируем отчет
        cmd = f'allure generate "{self.results_dir}" -o "{self.report_dir}" --clean'
        print(f"Выполняю: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
        print("✅ Отчет сгенерирован")

    def save_history(self):
        """Сохраняет отчет в историю"""
        print("💾 Сохранение в историю...")

        build_dir = self.history_dir / self.build_number
        build_dir.mkdir(parents=True, exist_ok=True)

        # Копируем отчет
        if self.report_dir.exists():
            for item in self.report_dir.glob("*"):
                try:
                    if item.is_dir():
                        shutil.copytree(item, build_dir / item.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, build_dir)
                except Exception as e:
                    print(f"⚠️ Ошибка копирования {item}: {e}")

        # Обновляем latest (Windows - через копирование)
        latest = self.history_dir / "latest"
        if latest.exists():
            shutil.rmtree(latest, ignore_errors=True)
        shutil.copytree(build_dir, latest)

        # Сохраняем метаданные
        meta = {
            "build_number": self.build_number,
            "timestamp": datetime.now().isoformat(),
            "passed": self._count_status("passed"),
            "failed": self._count_status("failed"),
            "broken": self._count_status("broken"),
            "skipped": self._count_status("skipped")
        }

        with open(build_dir / "meta.json", "w", encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        print(f"✅ История сохранена: {self.build_number}")

    def _count_status(self, status):
        """Подсчет тестов по статусу"""
        count = 0
        if self.results_dir.exists():
            for result_file in self.results_dir.glob("*-result.json"):
                try:
                    with open(result_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get("status") == status:
                            count += 1
                except:
                    pass
        return count

    def generate_index(self):
        """Генерирует index.html со списком запусков"""
        print("📝 Генерация index.html...")

        builds = sorted(
            [d for d in self.history_dir.iterdir()
             if d.is_dir() and d.name != "latest" and (d / "meta.json").exists()],
            reverse=True
        )[:20]

        html = """<!DOCTYPE html>
<html>
<head>
    <title>Allure Reports History</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e5e7eb;
        }
        h1 { 
            color: #1a1a2e;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle { 
            color: #666;
            font-size: 1.1em;
        }
        .run { 
            padding: 20px;
            margin: 15px 0;
            background: #f8fafc;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }
        .run:hover { 
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        .run-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .run a { 
            color: #2563eb;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.2em;
            transition: color 0.2s;
        }
        .run a:hover { 
            color: #1d4ed8;
            text-decoration: underline;
        }
        .timestamp { 
            color: #666;
            font-size: 0.9em;
        }
        .stats {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .stat {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }
        .passed { background: #dcfce7; color: #166534; }
        .failed { background: #fee2e2; color: #991b1b; }
        .broken { background: #fef3c7; color: #92400e; }
        .skipped { background: #f1f5f9; color: #475569; }
        .total-tests {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }
        .no-reports {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        .no-reports h2 {
            font-size: 3em;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Allure Test Reports</h1>
            <p class="subtitle">UI Tests History</p>
        </div>
"""

        if builds:
            for build in builds:
                try:
                    with open(build / "meta.json", 'r', encoding='utf-8') as f:
                        meta = json.load(f)

                    timestamp = datetime.fromisoformat(meta["timestamp"]).strftime("%d.%m.%Y %H:%M:%S")

                    stats_html = ""
                    for status, emoji in [("passed", "✅"), ("failed", "❌"),
                                          ("broken", "💥"), ("skipped", "⏭️")]:
                        count = meta.get(status, 0)
                        if count > 0:
                            stats_html += f'<span class="stat {status}">{emoji} {status}: {count}</span>'

                    total = sum(meta.get(s, 0) for s in ["passed", "failed", "broken", "skipped"])

                    html += f"""
            <div class="run">
                <div class="run-header">
                    <a href="{build.name}/index.html">📈 Build {meta['build_number']}</a>
                    <span class="timestamp">🕐 {timestamp}</span>
                </div>
                <div class="stats">{stats_html}</div>
            </div>"""
                except Exception as e:
                    print(f"⚠️ Ошибка обработки {build.name}: {e}")

            html += f'<div class="total-tests">📦 Total builds: {len(builds)}</div>'
        else:
            html += """
            <div class="no-reports">
                <h2>📭</h2>
                <p>No test reports yet</p>
                <p style="margin-top: 10px; color: #999;">Run the tests to generate the first report</p>
            </div>"""

        html += """
    </div>
</body>
</html>"""

        with open(self.history_dir / "index.html", "w", encoding='utf-8') as f:
            f.write(html)

        print("✅ index.html сгенерирован")

    def publish(self):
        """Публикация на GitHub Pages"""
        print("📤 Публикация на GitHub Pages...")

        if not self.history_dir.exists():
            print("❌ Нет истории для публикации")
            return False

        original_dir = os.getcwd()

        try:
            os.chdir(self.history_dir)

            # Проверяем, есть ли уже git
            if not (Path(".git").exists()):
                print("Инициализация git...")
                subprocess.run("git init", shell=True, check=True)

            # Создаем/переключаемся на ветку gh-pages
            subprocess.run("git checkout -b gh-pages 2>$null", shell=True)
            subprocess.run("git checkout gh-pages", shell=True)

            # Добавляем все файлы
            subprocess.run("git add .", shell=True, check=True)

            # Проверяем, есть ли изменения
            result = subprocess.run(
                "git status --porcelain",
                shell=True,
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                # Коммитим
                subprocess.run(
                    f'git commit -m "Update reports - {self.build_number}"',
                    shell=True,
                    check=True
                )

                # Добавляем remote если нужно
                result = subprocess.run(
                    "git remote get-url origin",
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    subprocess.run(
                        f"git remote add origin {self.repo_url}",
                        shell=True,
                        check=True
                    )

                # Пушим
                subprocess.run(
                    "git push -f origin gh-pages",
                    shell=True,
                    check=True
                )
                print("✅ Отчет опубликован!")
            else:
                print("ℹ️ Нет изменений для публикации")

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при публикации: {e}")
            return False
        finally:
            os.chdir(original_dir)

    def open_report(self):
        """Открывает отчет в браузере"""
        import webbrowser
        index_file = self.report_dir / "index.html"
        if index_file.exists():
            webbrowser.open(f"file://{index_file.absolute()}")
            print(f"🌐 Отчет открыт в браузере")

    def run(self, skip_tests=False, open_browser=True, publish=True):
        """Полный цикл"""
        exit_code = 0

        if not skip_tests:
            exit_code = self.run_tests()

        self.generate_report()
        self.save_history()
        self.generate_index()

        if publish:
            self.publish()

        if open_browser:
            self.open_report()

        print(f"\n{'=' * 60}")
        print(f"✅ Готово!")
        print(f"📁 Локальный отчет: {self.report_dir.absolute()}\\index.html")
        print(f"🌐 GitHub Pages: https://sergeysmorodin.github.io/UI_tests/")
        print(f"🔗 Этот запуск: https://sergeysmorodin.github.io/UI_tests/{self.build_number}/")
        print(f"{'=' * 60}")

        return exit_code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Allure Report Publisher')
    parser.add_argument('--skip-tests', action='store_true',
                        help='Пропустить запуск тестов (только сгенерировать отчет из существующих результатов)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Не открывать отчет в браузере')
    parser.add_argument('--no-publish', action='store_true',
                        help='Не публиковать на GitHub Pages')

    args = parser.parse_args()

    publisher = AllurePublisher(
        repo_url="https://github.com/SergeySmorodin/UI_tests.git"
    )

    exit(publisher.run(
        skip_tests=args.skip_tests,
        open_browser=not args.no_browser,
        publish=not args.no_publish
    ))