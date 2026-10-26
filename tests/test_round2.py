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

    def test_repository_root_and_directory_links(self):
        self.assertEqual(self.fixture('[root](/docs/README.md) [dir](docs/)', {'docs/README.md':'# Docs'}), [])
        self.assertTrue(self.fixture('[dir](empty/)', {'empty/note.txt':'not a readme'}))

    def test_json_cli_reports_errors_and_exit_status(self):
        import contextlib,io,json
        from scripts.check_links import main
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/'README.md').write_text('[bad](missing.md)')
            output=io.StringIO()
            with contextlib.redirect_stdout(output): code=main(['--root',folder,'--json'])
            self.assertEqual(code,1);self.assertFalse(json.loads(output.getvalue())['ok'])

    def test_code_fences_do_not_create_heading_anchors(self):
        for marker in ['```','~~~~']:
            self.assertTrue(self.fixture(f'{marker}md\n# Not a heading\n{marker}\n[bad](#not-a-heading)'))
            self.assertEqual(self.fixture(f'{marker}md\n# Same\n{marker}\n# Same\n[ok](#same)'),[])
        self.assertTrue(self.fixture('```md\n# Hidden\n````\n[bad](#hidden)'))

    def test_generated_duplicate_heading_links_and_json_parity(self):
        import contextlib,io,json
        from scripts.check_links import main
        for size in [1,2,10,30]:
            headings='\n'.join('# Same' for _ in range(size))
            links='\n'.join(f'[heading](#same{("-"+str(i)) if i else ""})' for i in range(size))
            self.assertEqual(self.fixture(headings+'\n'+links),[])
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'README.md').write_text('[bad](missing.md)')
            output=io.StringIO()
            with contextlib.redirect_stdout(output):status=main(['--root',str(root),'--json'])
            self.assertEqual(status,1);self.assertEqual(json.loads(output.getvalue())['errors'],check(root))
