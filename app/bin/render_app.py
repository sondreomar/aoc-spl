import os
import subprocess
from pathlib import Path

import jinja2

APP = Path("app")
SOLUTIONS = Path("solutions")


def render_templates(app: Path, spl_files: Path):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([app, spl_files]),
        keep_trailing_newline=True,
    )
    savedsearches = [spl.relative_to(spl_files).as_posix() for spl in spl_files.rglob("*.spl")]
    for path in APP.rglob("*.j2"):
        template = env.get_template(path.relative_to(app).as_posix())
        with open(path.with_suffix(""), "w") as f:
            f.write(env.get_template(template).render(savedsearches=sorted(savedsearches)))


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
