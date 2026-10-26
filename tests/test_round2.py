from pathlib import Path
import tempfile
import unittest
from scripts.check_links import check

class LinkExtensions(unittest.TestCase):
    def fixture(self, content, other=None):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text(content)
            for path,text in (other or {}).items():
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
            return check(root)

    def test_code_examples_are_not_navigation(self):
        self.assertEqual(self.fixture('```md\n[example](missing.md)\n```\n`[inline](missing.md)`'), [])

    def test_heading_fragments_are_checked(self):
        self.assertEqual(self.fixture('# Overview\n[ok](#overview)'), [])
        self.assertTrue(self.fixture('# Overview\n[bad](#missing)'))
        self.assertEqual(self.fixture('# Same\n# Same\n[ok](#same-1)'), [])

    def test_reference_style_links(self):
        self.assertEqual(self.fixture('[guide][g]\n[g]: GUIDE.md', {'GUIDE.md':'# Guide'}), [])
        self.assertTrue(self.fixture('[broken][missing]'))
