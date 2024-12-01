import subprocess
from pathlib import Path

import jinja2

APP = Path("advent-of-code")
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
            f.write(env.get_template(template).render(savedsearches=savedsearches))


def reload_splunk_app(app: Path):
    subprocess.run(
        [
            f"/opt/splunk/bin/splunk _internal call /services/apps/local/{app.stem}/_reload",
            "-auth admin:$SPLUNK_PASSWORD",
        ],
        shell=True,
        stderr=subprocess.PIPE,
        check=True,
    )


def main():
    render_templates(APP, SOLUTIONS)
    try:
        reload_splunk_app(APP)
    except subprocess.SubprocessError:
        pass
    else:
        print(f"{APP} reloaded")


if __name__ == "__main__":
    main()
