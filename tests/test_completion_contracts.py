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

    def test_018_inline_code_links_are_not_navigation(self):
        self.fixture('`[example](missing.md)`',{},True)

    def test_019_backtick_fenced_links_are_not_navigation(self):
        self.fixture('```md\n[example](missing.md)\n```',{},True)

    def test_020_tilde_fenced_links_are_not_navigation(self):
        self.fixture('~~~~md\n[example](missing.md)\n~~~~',{},True)

    def test_021_longer_closing_fences_close_code_examples(self):
        self.fixture('```md\n[example](missing.md)\n````\n[ok](README.md)',{},True)

    def test_022_fenced_headings_do_not_create_fragments(self):
        self.fixture('```md\n# Hidden\n```\n[link](#hidden)',{},False)

    def test_023_external_https_destinations_are_not_fetched(self):
        self.fixture('[external](https://example.invalid/missing)',{},True)

    def test_024_external_http_destinations_are_not_fetched(self):
        self.fixture('[external](http://example.invalid/missing)',{},True)

    def test_025_mailto_destinations_are_not_local_files(self):
        self.fixture('[email](mailto:hello@example.test)',{},True)

    def test_026_protocol_relative_links_are_not_local_paths(self):
        self.fixture('[external](//example.invalid/path)',{},True)

    def test_027_reference_style_links_resolve_definitions(self):
        self.fixture('[guide][g]\n[g]: guide.md',{'guide.md': '# Guide'},True)

    def test_028_reference_labels_match_case_insensitively(self):
        self.fixture('[guide][GUIDE]\n[guide]: guide.md',{'guide.md': '# Guide'},True)

    def test_029_collapsed_reference_labels_use_link_text(self):
        self.fixture('[guide][]\n[guide]: guide.md',{'guide.md': '# Guide'},True)

    def test_030_missing_reference_definitions_fail(self):
        self.fixture('[guide][missing]',{},False)

    def test_031_markdown_images_resolve_local_sources(self):
        self.fixture('![icon](assets/icon.txt)',{'assets/icon.txt': 'data'},True)

    def test_032_missing_markdown_image_sources_fail(self):
        self.fixture('![icon](assets/missing.png)',{},False)

    def test_033_html_images_resolve_local_sources(self):
        self.fixture('<img src="icon.txt">',{'icon.txt': 'data'},True)

    def test_034_missing_html_image_sources_fail(self):
        self.fixture('<img src="missing.png">',{},False)

    def test_035_svg_fragments_resolve_element_ids(self):
        self.fixture('[icon](icon.svg#mark)',{'icon.svg': '<svg><g id="mark"/></svg>'},True)

    def test_036_svg_missing_fragments_fail(self):
        self.fixture('[icon](icon.svg#missing)',{'icon.svg': '<svg><g id="mark"/></svg>'},False)

    def test_037_malformed_svg_targets_fail_cleanly(self):
        self.fixture('[icon](icon.svg#mark)',{'icon.svg': '<svg>'},False)

    def test_038_links_after_closed_fences_are_still_checked(self):
        self.fixture('```\nexample\n```\n[missing](no.md)',{},False)

    def test_039_plain_text_without_links_is_valid(self):
        self.fixture('A normal paragraph.',{},True)

    def test_040_code_fences_with_language_tags_are_ignored(self):
        self.fixture('```typescript\n[not a link](missing.md)\n```',{},True)

    def test_041_headings_with_inline_code_keep_visible_names(self):
        self.fixture('# Use `Client`\n[link](#use-client)',{},True)

    def test_042_heading_case_normalization_preserves_unicode_letters(self):
        self.fixture('# Straße\n[link](#straße)',{},True)

    def test_043_fragment_only_links_stay_in_the_current_document(self):
        self.fixture('# Root\n[ok](#root)',{},True)

    def test_044_root_directory_targets_use_repository_readme(self):
        self.fixture('[root](/)',{},True)
