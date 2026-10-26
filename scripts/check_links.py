"""Validate local Markdown links and inline image sources without network access."""
from pathlib import Path
import re
import os
import html
from urllib.parse import unquote, urlsplit
import sys
import argparse
import json
import xml.etree.ElementTree as ET


def without_fences(text: str) -> str:
    """Ignore fenced examples, including fences closed by a longer marker."""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line.rstrip('\r\n'))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker and (marker[1][0] != '`' or '`' not in marker[2]):
            fence = (marker[1][0], len(marker[1]))
            continue
        lines.append(line)
    return ''.join(lines)


def anchors(text: str) -> set[str]:
    text = without_fences(text)
    found=set(); counts={}
    for heading in re.findall(r'^ {0,3}#{1,6}\s+(.+?)\s*#*$', text, re.M):
        slug=re.sub(r'[^\w -]', '', heading.casefold()).replace(' ', '-')
        index=counts.get(slug,0);counts[slug]=index+1
        found.add(slug if not index else f'{slug}-{index}')
    found.update(re.findall(r'\bid=[\'"]([^\'"]+)', text))
    return found


def markdown_sources(root: Path):
    ignored = {'.git', 'node_modules', '.venv', '__pycache__'}
    for directory, folders, files in os.walk(root, followlinks=False):
        folders[:] = sorted(name for name in folders if name not in ignored)
        for name in sorted(files):
            if name.endswith('.md'): yield Path(directory) / name


def check(root: Path) -> list[str]:
    errors = []
    for source in markdown_sources(root):
        text = source.read_text(encoding='utf-8')
        text = without_fences(text)
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
