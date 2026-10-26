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

    def test_004_directory_targets_resolve_readme_files(self):
        self.fixture('[docs](docs/)',{'docs/README.md': '# Docs'},True)

    def test_005_directories_without_readmes_are_not_valid_documents(self):
        self.fixture('[docs](docs/)',{'docs/file.txt': 'text'},False)

    def test_006_percent_encoded_spaces_in_local_paths_resolve(self):
        self.fixture('[guide](my%20guide.md)',{'my guide.md': '# Guide'},True)

    def test_007_query_parameters_do_not_change_local_file_resolution(self):
        self.fixture('[guide](guide.md?view=1)',{'guide.md': '# Guide'},True)

    def test_008_same_file_fragments_resolve(self):
        self.fixture('## Details\n[link](#details)',{},True)

    def test_009_missing_same_file_fragments_fail(self):
        self.fixture('## Details\n[link](#absent)',{},False)

    def test_010_cross_file_fragments_resolve(self):
        self.fixture('[link](guide.md#details)',{'guide.md': '## Details'},True)

    def test_011_missing_cross_file_fragments_fail(self):
        self.fixture('[link](guide.md#absent)',{'guide.md': '## Details'},False)

    def test_012_unicode_fragments_decode_before_slug_checks(self):
        self.fixture('## Café\n[link](#caf%C3%A9)',{},True)

    def test_013_duplicate_headings_receive_numbered_suffixes(self):
        self.fixture('# Same\n# Same\n# Same\n[link](#same-2)',{},True)

    def test_014_heading_links_use_visible_text_for_slugs(self):
        self.fixture('# [API](https://example.test)\n[link](#api)',{},True)

    def test_015_heading_html_uses_visible_text_for_slugs(self):
        self.fixture('# <b>API</b>\n[link](#api)',{},True)

    def test_016_heading_entities_are_unescaped_before_slugging(self):
        self.fixture('# A &amp; B\n[link](#a--b)',{},True)

    def test_017_explicit_html_ids_can_be_linked(self):
        self.fixture('<div id="custom"></div>\n[link](#custom)',{},True)
