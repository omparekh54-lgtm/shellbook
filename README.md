# Shellbook

Shellbook is a lightweight Python reference library for course theory, Django code, Docker commands, and Git commands.

## Install locally

```bash
pip install .
```

## Run

```bash
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

Direct access:

```bash
shellbook 1
shellbook 2
shellbook 3
shellbook 4
shellbook 5
```

Open the exact bundled source PDF for sections 1-4:

```bash
shellbook 1 --pdf
```

## Python API

```python
from shellbook import get_text, list_sections
print(list_sections())
print(get_text(3))
```

The four supplied source PDFs are bundled inside the package.
