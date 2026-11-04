import tempfile,unittest
from pathlib import Path
from scripts.check_links import check
class MarkdownExtensions(unittest.TestCase):
    def test_uppercase_and_long_extensions_are_validated(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text('[topic](TOPIC.MARKDOWN#topic)');(root/'TOPIC.MARKDOWN').write_text('# Topic')
            self.assertEqual(check(root),[])
            (root/'BROKEN.MD').write_text('[bad](missing.md)')
            self.assertTrue(any('BROKEN.MD' in e for e in check(root)))
            (root/'BROKEN.MD').unlink();(root/'TOPIC.MARKDOWN').write_text('# Other')
            self.assertTrue(any('missing anchor' in e for e in check(root)))
