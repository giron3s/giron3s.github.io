import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml  # type: ignore
from jinja2 import Environment, FileSystemLoader


class Portfolio:
    def __init__(self):
        self.config_files = {
            "profile": "config/profile.yml",
            "about": "config/about.yml",
            "resume": "config/experience.yml",
            "projects": "config/projects.yml",
            "blog": "config/blog.yml",
            "contact": "config/contact.yml",
            "navbar": "config/navbar.yml",
            "skills": "config/skills.yml",
        }
        self.env = Environment(loader=FileSystemLoader("src/jinja"))
        self.env.filters["format_date"] = self.format_date

    def read_file(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def write_file(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def load_config_file(self, file_key: str) -> dict[str, Any]:
        file_path = self.config_files.get(file_key)
        content = self.read_file(file_path)
        return yaml.load(content, Loader=yaml.FullLoader)

    def asset_version(self) -> str:
        """Short content hash of the static assets, used to bust browser caches.

        Asset paths never change between deploys, so browsers keep serving a
        stale style.css or icon. Appending this hash to their URLs makes the
        browser refetch them only when their content actually changed.
        """
        digest = hashlib.md5()
        paths = [Path("src/css/style.css")]
        paths += sorted(Path("config/assets/icons").glob("*.svg"))
        for path in paths:
            if path.is_file():
                digest.update(path.read_bytes())
        return digest.hexdigest()[:8]

    def format_date(self, date_str: str) -> str:
        date_object = datetime.strptime(date_str, "%Y-%m-%d")
        return date_object.strftime("%b %d, %Y")

    def render_template(
        self, template_name: str, output_path: str, context: dict[str, Any]
    ) -> None:
        template = self.env.get_template(template_name)
        html_render = template.render(context)
        self.write_file(output_path, html_render)


if __name__ == "__main__":
    portfolio = Portfolio()
    context = {key: portfolio.load_config_file(key) for key in portfolio.config_files}
    context["asset_version"] = portfolio.asset_version()
    portfolio.render_template("index.j2", "index.html", context)
