"""Shellbook command line menu."""
import argparse
import pydoc
import sys
import subprocess
from . import __version__
from .reference import SECTIONS, get_text, search, export_pdf, open_pdf


def display(section, plain=False):
    text = SECTIONS[section][0] + "\n" + "=" * 42 + "\n\n" + get_text(section)
    if plain or not sys.stdout.isatty():
        print(text)
    else:
        pydoc.pager(text)


def menu(plain=False, pdf=False):
    while True:
        print("\nSHELLBOOK\n" + "=" * 42)
        for number, (title, _) in SECTIONS.items():
            print(f"{number}. {title}")
        print("0. Exit\n" + "=" * 42)
        try:
            choice = input("Enter option (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if choice == "0":
            return 0
        if choice not in {str(n) for n in SECTIONS}:
            print("Please enter a number from 1 to 5, or 0 to exit.")
            continue
        try:
            if pdf:
                print(f"Opened: {open_pdf(int(choice))}")
            else:
                display(int(choice), plain)
        except (ValueError, OSError, subprocess.CalledProcessError) as exc:
            print(f"Cannot open section: {exc}", file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Shellbook offline study reference")
    parser.add_argument("section", nargs="?", type=int, choices=SECTIONS, help="section number (1-5)")
    parser.add_argument("--version", action="version", version=f"Shellbook {__version__}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pdf", action="store_true", help="open the original PDF in your default viewer")
    group.add_argument("--export-pdf", metavar="PATH", help="save the original PDF to PATH")
    group.add_argument("--search", metavar="TEXT", help="search all references, or the selected section")
    parser.add_argument("--plain", action="store_true", help="print without an interactive pager")
    args = parser.parse_args(argv)
    if args.export_pdf and args.section is None:
        parser.error("--export-pdf requires a section number")
    try:
        if args.search is not None:
            matches = search(args.search, args.section)
            for section, line, text in matches:
                print(f"{SECTIONS[section][0]}:{line}: {text}")
            if not matches:
                print("No matches found.")
            return 0
        if args.section is None:
            return menu(args.plain, args.pdf)
        if args.export_pdf:
            print(export_pdf(args.section, args.export_pdf))
        elif args.pdf:
            print(f"Opened: {open_pdf(args.section)}")
        else:
            display(args.section, args.plain)
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Shellbook: {exc}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, BrokenPipeError):
        return 0
