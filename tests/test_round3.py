from pathlib import Path
import tempfile,unittest
from scripts.check_links import check,anchors
class LinkRound3(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);(self.root/'README.md').write_text('# Root')
    def tearDown(self):self.temp.cleanup()
    def test_dependency_and_cache_directories_are_not_traversed(self):
        for folder in ['.git','node_modules','.venv','__pycache__']:
            target=self.root/folder/'deep';target.mkdir(parents=True);(target/'bad.md').write_text('[bad](missing.md)')
        self.assertEqual(check(self.root),[])
    def test_bad_utf8_becomes_a_diagnostic_instead_of_a_traceback(self):
        (self.root/'bad.md').write_bytes(b'\xff')
        self.assertTrue(any('unreadable Markdown' in message for message in check(self.root)))
    def test_heading_slugs_follow_visible_link_and_html_text(self):
        self.assertIn('read-the-guide',anchors('# Read [the guide](https://example.test)'))
        self.assertIn('a--b',anchors('# <span>A &amp; B</span>'))
        self.assertIn('straße',anchors('# Straße'))
    def test_parent_and_symlink_escapes_are_not_machine_specific_successes(self):
        with tempfile.TemporaryDirectory() as external:
            outside=Path(external)/'guide.md';outside.write_text('# Outside')
            (self.root/'outside.md').symlink_to(outside)
            (self.root/'README.md').write_text('[escape](outside.md)')
            self.assertTrue(any('outside repository' in error for error in check(self.root)))
    def test_svg_fragment_links_resolve_real_element_ids(self):
        (self.root/'icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><g id="mark"/></svg>')
        (self.root/'README.md').write_text('[ok](icon.svg#mark)');self.assertEqual(check(self.root),[])
        (self.root/'README.md').write_text('[bad](icon.svg#absent)');self.assertTrue(any('missing SVG anchor' in message for message in check(self.root)))
