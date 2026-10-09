# Shellbook

An offline Python library and terminal reference containing the complete supplied Unit 2 and Unit 5 notes, code manuals, and an additional Git cheat sheet. No API key, Django installation, Docker installation, or internet connection is needed after installation. References are displayed as text; code and commands are never executed.

## Install

Requires Python 3.9 or newer. Install directly from this repository:

```sh
python -m pip install git+https://github.com/omparekh54-lgtm/shellbook.git
```

This method requires Git. Alternatively download the repository ZIP, extract it, open a terminal inside the extracted folder and run:

```sh
python -m pip install .
```

The package is not published to PyPI yet.

## Use

```sh
shellbook
```

```text
SHELLBOOK
==========================================
1. Unit 2 Theory
2. Unit 5 Theory
3. Django Code
4. Docker Commands
5. Git Commands
0. Exit
==========================================
Enter option (1-5):
```

Enter a number to read its section. In an interactive terminal, long references open in a pager; press `q` to return to the menu. Choose `0` to exit. If the command is not on your PATH, use `python -m shellbook` instead.

```sh
shellbook 1                       # Unit 2 theory
shellbook 2                       # Unit 5 theory
shellbook 3                       # Complete Unit 2 coding manual (including Django)
shellbook 4                       # Complete Docker coding manual
shellbook 5                       # Git cheat sheet
shellbook 3 --plain               # Print without paging
shellbook 1 --pdf                 # Open the original PDF
shellbook 4 --export-pdf docker.pdf
shellbook --search migrations     # Search all five sections
shellbook 3 --search runserver    # Search one section
```

The four original PDFs are bundled unchanged. Extracted text preserves all pages, with page separators; tables or diagrams may display better in the original PDF. Option 3 includes Python, networking and other code from the complete Unit 2 manual so none of its content is omitted. Option 5 is an extra text reference and has no original PDF. PDF opening requires a desktop PDF viewer; use `--export-pdf` on a headless machine. Export writes to the specified destination and replaces an existing file there.

## Python API

```python
from shellbook import get_text, search

print(get_text(1))
for section, line_number, text in search("Docker"):
    print(section, line_number, text)
```

## Development

```sh
python -m pip install .
python -m unittest discover -s tests -v
python -m pip wheel --no-deps . -w dist
```

Source PDFs retain their original authorship. The Git reference is supplementary material.
