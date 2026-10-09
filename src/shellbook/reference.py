"""Read packaged references without any runtime dependencies."""
from importlib.resources import files
from pathlib import Path
import os
import subprocess
import sys

SECTIONS = {
    1: ("Unit 2 Theory", "unit2_theory"),
    2: ("Unit 5 Theory", "unit5_theory"),
    3: ("Django Code", "django_code"),
    4: ("Docker Commands", "docker_commands"),
    5: ("Git Commands", "git_commands"),
}


def resource(section, suffix="txt"):
    if section not in SECTIONS:
        raise ValueError("Choose a section from 1 to 5.")
    if suffix == "pdf" and section == 5:
        raise ValueError("Git Commands is a text reference; it has no source PDF.")
    return files("shellbook").joinpath("data", SECTIONS[section][1] + "." + suffix)


def get_text(section):
    """Return the complete reference text for a section numbered 1 to 5."""
    return resource(section).read_text(encoding="utf-8")


def search(query, section=None):
    """Return (section, line number, text) matches, ignoring case."""
    if not query.strip():
        raise ValueError("Enter a non-empty search query.")
    matches = []
    for number in ([section] if section is not None else SECTIONS):
        for line_number, line in enumerate(get_text(number).splitlines(), 1):
            if query.casefold() in line.casefold():
                matches.append((number, line_number, line.strip()))
    return matches


def export_pdf(section, destination):
    """Copy an original PDF to a persistent destination."""
    content = resource(section, "pdf").read_bytes()
    path = Path(destination).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path.resolve()


def open_pdf(section):
    """Save a stable local copy before launching the OS PDF viewer."""
    root = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".cache")) / "shellbook" / "1.0.0"
    path = export_pdf(section, root / (SECTIONS[section][1] + ".pdf"))
    if sys.platform == "win32":
        os.startfile(str(path))
    else:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)], check=True)
    return path
