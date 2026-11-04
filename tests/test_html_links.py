import tempfile,unittest
from pathlib import Path
from scripts.check_links import check
class HtmlLinks(unittest.TestCase):
    def test_local_html_hyperlinks_receive_the_same_checks(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text('<A class="link" HREF="topic.md#topic">Read</A>')
            (root/'topic.md').write_text('# Topic')
            self.assertEqual(check(root),[])
            (root/'topic.md').write_text('# Other')
            self.assertTrue(any('missing anchor' in e for e in check(root)))
            (root/'README.md').write_text('<a href="../outside.md">Outside</a>')
            self.assertTrue(any('outside repository' in e for e in check(root)))
