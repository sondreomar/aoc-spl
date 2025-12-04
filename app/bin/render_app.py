import json
import os
import subprocess
from pathlib import Path

import jinja2

APP = Path("app")
SOLUTIONS = Path("solutions")


def render_templates(app: Path, spl_path: Path):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([app, spl_path]),
        keep_trailing_newline=True,
    )
    for path in APP.rglob("*.j2"):
        template = env.get_template(path.relative_to(app).as_posix())
        with open(path.with_suffix(""), "w") as f:
            f.write(
                env.get_template(template).render(
                    splnbsearches=get_splnbsearches(spl_path),
                    savedsearches=sorted(get_savedsearches(spl_path)),
                )
            )


def get_savedsearches(path: Path) -> list[str]:
    return [spl.relative_to(path).as_posix() for spl in path.rglob("*.spl")]


def get_splnbsearches(path: Path) -> dict[str, str]:
    splnb_searches = {}
    for f in path.rglob("*.splnb"):
        splnb_searches.update(splnb_to_searches(f))
    return splnb_searches


def splnb_to_searches(path: Path) -> dict[str, str]:
    with open(path, "r") as f:
        cells = [x for line in f.readlines() for x in json.loads(line) if line.strip()]
        searches = {}
        for i, cell in enumerate(cells):
            if cell.get("language") != "splunk_search":
                continue
            if cell.get("value").strip() == "":
                continue
            key = path.relative_to(SOLUTIONS).as_posix()
            if len(cells) > 1:
                key = f"{key}[{i}]"
            searches[key] = cell.get("value")
    return searches


def reload_splunk_app(app: Path):
    subprocess.run(
        [
            "/opt/splunk/bin/splunk",
            "_internal",
            "call",
            f"/services/apps/local/{app.stem}/_reload",
            "-auth",
            f"admin:{os.environ['SPLUNK_PASSWORD']}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        check=True,
    )


def main():
    render_templates(APP, SOLUTIONS)
    if "SPLUNK_HOME" not in os.environ:
        exit()
    try:
        reload_splunk_app(APP)
    except subprocess.SubprocessError as e:
        print(e)
    else:
        print(f"{APP} reloaded")


if __name__ == "__main__":
    main()
