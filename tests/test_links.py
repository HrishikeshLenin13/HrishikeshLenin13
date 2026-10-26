import importlib.util
from pathlib import Path
import tempfile
import unittest
spec = importlib.util.spec_from_file_location('links', Path(__file__).resolve().parents[1] / 'scripts/check_links.py')
links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(links)

class LinkTests(unittest.TestCase):
    def test_current_profile(self):
        self.assertEqual(links.check(Path(__file__).resolve().parents[1]), [])

    def test_detects_missing_markdown_and_html_images(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'README.md').write_text('[bad](missing.md) <img src="missing.svg">')
            self.assertEqual(len(links.check(root)), 2)

    def test_allows_external_and_fragment_links_and_encoded_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'a b.md').write_text('ok')
            (root / 'README.md').write_text('# title\n[web](https://example.org/a) [part](#title) [local](a%20b.md)')
            self.assertEqual(links.check(root), [])

    def test_invalid_svg_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'assets').mkdir()
            (root / 'assets/header.svg').write_text('<svg>')
            self.assertIn('invalid SVG', links.check(root)[0])
