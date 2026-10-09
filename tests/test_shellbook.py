import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from shellbook import get_text, search
from shellbook.cli import main
from shellbook.reference import export_pdf, resource


class ShellbookTests(unittest.TestCase):
    def run_cli(self, args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = main(args)
        return code, out.getvalue()

    def test_all_five_sections_available(self):
        for number in range(1, 6):
            with self.subTest(number=number):
                self.assertGreater(len(get_text(number)), 1000)
                code, text = self.run_cli([str(number), '--plain'])
                self.assertEqual(code, 0)
                self.assertIn(get_text(number), text)

    def test_menu_invalid_then_read_then_exit(self):
        with patch('builtins.input', side_effect=['bad', '3', '0']):
            code, text = self.run_cli(['--plain'])
        self.assertEqual(code, 0)
        self.assertIn('Please enter', text)
        self.assertIn('runserver', text)

    def test_eof_exits(self):
        with patch('builtins.input', side_effect=EOFError):
            self.assertEqual(self.run_cli([])[0], 0)

    def test_search_is_case_insensitive_and_scoped(self):
        self.assertEqual(search('RUNSERVER', 3), search('runserver', 3))
        self.assertTrue(search('runserver', 3))
        self.assertTrue(all(row[0] == 3 for row in search('runserver', 3)))
        self.assertIn('No matches found.', self.run_cli(['--search', 'xyzneverfound123'])[1])
        self.assertEqual(self.run_cli(['--search', ''])[0], 1)

    def test_pdf_export_exact_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            for number in range(1, 5):
                path = export_pdf(number, Path(folder) / f'{number}.pdf')
                self.assertEqual(path.read_bytes(), resource(number, 'pdf').read_bytes())
                self.assertTrue(path.read_bytes().startswith(b'%PDF-'))

    def test_git_has_no_pdf(self):
        self.assertEqual(self.run_cli(['5', '--pdf'])[0], 1)
        with self.assertRaises(ValueError):
            get_text(6)


if __name__ == '__main__':
    unittest.main()
