"""Validate local Markdown links and inline image sources without network access."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import sys
import argparse
import json
import xml.etree.ElementTree as ET


def anchors(text: str) -> set[str]:
    found=set(); counts={}
    for heading in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug=re.sub(r'[^\w -]', '', heading.casefold()).replace(' ', '-')
        index=counts.get(slug,0);counts[slug]=index+1
        found.add(slug if not index else f'{slug}-{index}')
    found.update(re.findall(r'\bid=[\'"]([^\'"]+)', text))
    return found


def check(root: Path) -> list[str]:
    errors = []
    for source in sorted(root.rglob('*.md')):
        if '.git' in source.parts:
            continue
        text = source.read_text(encoding='utf-8')
        text = re.sub(r'(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[ \t]*$', '', text)
        text = re.sub(r'`+[^`]*`+', '', text)
        links = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text)
        definitions = {key.strip().casefold(): value for key,value in re.findall(r'^ {0,3}\[([^\]]+)\]:\s*(\S+)', text, re.M)}
        for label, reference in re.findall(r'!?\[([^\]]+)\]\[([^\]]*)\]', text):
            key=(reference or label).strip().casefold()
            if key not in definitions: errors.append(f'{source.relative_to(root)}: undefined reference {key}')
            else: links.append(definitions[key])
        links += re.findall(r'<img[^>]+src=[\'"]([^\'"]+)', text, re.I)
        for link in links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            target = (root / unquote(parts.path).lstrip("/")) if parts.path.startswith("/") else (source.parent / unquote(parts.path) if parts.path else source)
            if target.is_dir():
                target = target / "README.md"
            if not target.is_file():
                errors.append(f'{source.relative_to(root)}: missing {link}')
            elif parts.fragment and target.suffix.lower() == '.md' and unquote(parts.fragment) not in anchors(target.read_text(encoding='utf-8')):
                errors.append(f'{source.relative_to(root)}: missing anchor {link}')
    for source in sorted((root / 'assets').glob('*.svg')):
        try:
            ET.parse(source)
        except ET.ParseError as error:
            errors.append(f'{source.relative_to(root)}: invalid SVG: {error}')
    return errors

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true', help='emit machine-readable diagnostics')
    args=parser.parse_args(argv)
    if not args.root.is_dir(): parser.error('root must be a directory')
    errors=check(args.root.resolve())
    print(json.dumps({'ok':not errors,'errors':errors}) if args.json else ('\n'.join(errors) if errors else 'Local links and SVG assets are valid.'))
    return int(bool(errors))

if __name__ == '__main__':
    sys.exit(main())
