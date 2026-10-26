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
