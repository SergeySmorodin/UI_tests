#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path


class AllurePublisher:
    def __init__(self, repo_url, results_dir="allure-results",
                 report_dir="allure-report", history_dir="allure-history"):
        self.repo_url = repo_url
        self.results_dir = Path(results_dir)
        self.report_dir = Path(report_dir)
        self.history_dir = Path(history_dir)
        self.build_number = datetime.now().strftime("%Y%m%d-%H%M%S")

    def run_tests(self):
        return subprocess.run(
            ["poetry", "run", "pytest", "-n", "auto", "--dist", "loadscope",
             f"--alluredir={self.results_dir}", "-v"],
            shell=True
        ).returncode

    def generate_report(self):
        latest = self.history_dir / "latest"
        if latest.is_dir():
            history_src = latest / "history"
            if history_src.exists():
                history_dst = self.results_dir / "history"
                history_dst.mkdir(exist_ok=True)
                for f in history_src.glob("*"):
                    if f.is_file():
                        shutil.copy2(f, history_dst)

        subprocess.run(
            f'allure generate "{self.results_dir}" -o "{self.report_dir}" --clean',
            shell=True, check=True
        )

    def save_history(self):
        build_dir = self.history_dir / self.build_number
        build_dir.mkdir(parents=True, exist_ok=True)

        if self.report_dir.exists():
            for item in self.report_dir.glob("*"):
                try:
                    if item.is_dir():
                        shutil.copytree(item, build_dir / item.name, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, build_dir)
                except Exception:
                    pass

        latest = self.history_dir / "latest"
        if latest.exists():
            shutil.rmtree(latest, ignore_errors=True)
        shutil.copytree(build_dir, latest)

        meta = {
            "build_number": self.build_number,
            "timestamp": datetime.now().isoformat(),
            "passed": self._count_status("passed"),
            "failed": self._count_status("failed"),
            "broken": self._count_status("broken"),
            "skipped": self._count_status("skipped")
        }
        with open(build_dir / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    def _count_status(self, status):
        count = 0
        if self.results_dir.exists():
            for result_file in self.results_dir.glob("*-result.json"):
                try:
                    with open(result_file, "r", encoding="utf-8") as f:
                        if json.load(f).get("status") == status:
                            count += 1
                except Exception:
                    pass
        return count

    def generate_index(self):
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
        h1 { color: #1a1a2e; font-size: 2.5em; }
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
        }
        .run a:hover { text-decoration: underline; }
        .timestamp { color: #666; font-size: 0.9em; }
        .stats { display: flex; gap: 15px; flex-wrap: wrap; }
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
        .no-reports {
            text-align: center;
            padding: 60px 20px;
            color: #666;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Allure Test Reports</h1>
        </div>
"""

        if builds:
            for build in builds:
                with open(build / "meta.json", "r", encoding="utf-8") as f:
                    meta = json.load(f)

                timestamp = datetime.fromisoformat(meta["timestamp"]).strftime("%d.%m.%Y %H:%M:%S")

                stats_html = ""
                for status, emoji in [("passed", "✅"), ("failed", "❌"),
                                      ("broken", "💥"), ("skipped", "⏭️")]:
                    count = meta.get(status, 0)
                    if count > 0:
                        stats_html += f'<span class="stat {status}">{emoji} {count}</span>'

                html += f"""
            <div class="run">
                <div class="run-header">
                    <a href="{build.name}/index.html">📈 Build {meta['build_number']}</a>
                    <span class="timestamp">🕐 {timestamp}</span>
                </div>
                <div class="stats">{stats_html}</div>
            </div>"""
        else:
            html += '<div class="no-reports">📭 No test reports yet</div>'

        html += """
    </div>
</body>
</html>"""

        with open(self.history_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html)

    def publish(self):
        if not self.history_dir.exists():
            return False

        original_dir = os.getcwd()
        try:
            os.chdir(self.history_dir)

            if not Path(".git").exists():
                subprocess.run("git init", shell=True, check=True)

            result = subprocess.run("git branch --list gh-pages", shell=True,
                                    capture_output=True, text=True)
            if "gh-pages" in result.stdout:
                subprocess.run("git checkout gh-pages", shell=True, check=True)
            else:
                subprocess.run("git checkout -b gh-pages", shell=True, check=True)

            subprocess.run("git add .", shell=True, check=True)

            result = subprocess.run("git status --porcelain", shell=True,
                                    capture_output=True, text=True)
            if result.stdout.strip():
                subprocess.run(f'git commit -m "Update reports - {self.build_number}"',
                               shell=True, check=True)

                # Всегда обновляем remote на актуальный
                result = subprocess.run("git remote get-url origin", shell=True,
                                        capture_output=True, text=True)
                if result.returncode != 0:
                    subprocess.run(f"git remote add origin {self.repo_url}",
                                   shell=True, check=True)
                else:
                    # Обновляем URL, если он изменился
                    subprocess.run(f"git remote set-url origin {self.repo_url}",
                                   shell=True, check=True)

                subprocess.run("git push -f origin gh-pages", shell=True, check=True)

            return True
        except subprocess.CalledProcessError:
            return False
        finally:
            os.chdir(original_dir)

    def open_report(self):
        index_file = self.report_dir / "index.html"
        if index_file.exists():
            webbrowser.open(f"file://{index_file.absolute()}")

    def run(self, skip_tests=False, open_browser=True, publish=True):
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

        return exit_code


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--no-publish", action="store_true")
    parser.add_argument("--repo-url", default="https://github.com/SergeySmorodin/UI_tests.git")
    args = parser.parse_args()

    publisher = AllurePublisher(repo_url=args.repo_url)
    publisher.run(
        skip_tests=args.skip_tests,
        open_browser=not args.no_browser,
        publish=not args.no_publish
    )
