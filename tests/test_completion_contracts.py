from pathlib import Path
import tempfile,unittest
from scripts.check_links import check
class CompletionContracts(unittest.TestCase):
    def fixture(self,text,files,ok):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text(text)
            for name,body in files.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
            errors=check(root)
            self.assertEqual(not errors,ok,errors)

    def test_001_relative_markdown_destinations_resolve(self):
        self.fixture('[guide](docs/guide.md)',{'docs/guide.md': '# Guide'},True)

    def test_002_missing_relative_files_fail(self):
        self.fixture('[missing](no.md)',{},False)

    def test_003_repository_root_links_resolve_from_nested_files(self):
        self.fixture('[nested](docs/n.md)',{'docs/n.md': '[root](/README.md)'},True)
