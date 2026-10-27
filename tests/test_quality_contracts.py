from pathlib import Path
import tempfile,unittest
from scripts.check_links import check
class QualityContracts(unittest.TestCase):
    def fixture(self,text,files,ok):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text(text)
            for name,body in files.items():
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(body)
            errors=check(root)
            self.assertEqual(not errors,ok,errors)

    def test_001_encoded_local_path_1(self):
        self.fixture('[x](one.md#target)',{'one.md':'# Target'},True)

    def test_002_encoded_local_path_2(self):
        self.fixture('[x](docs/one.md#target)',{'docs/one.md':'# Target'},True)

    def test_003_encoded_local_path_3(self):
        self.fixture('[x](two%20words.md#target)',{'two words.md':'# Target'},True)

    def test_004_encoded_local_path_4(self):
        self.fixture('[x](caf%C3%A9.md#target)',{'café.md':'# Target'},True)
