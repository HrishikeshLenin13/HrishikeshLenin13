"""Validate local Markdown links and inline image sources without network access."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import sys
import xml.etree.ElementTree as ET


def check(root: Path) -> list[str]:
    errors = []
    for source in sorted(root.rglob('*.md')):
        if '.git' in source.parts:
            continue
        text = source.read_text(encoding='utf-8')
        links = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text)
        links += re.findall(r'<img[^>]+src=[\'"]([^\'"]+)', text, re.I)
        for link in links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = source.parent / unquote(parts.path)
            if not target.is_file():
                errors.append(f'{source.relative_to(root)}: missing {link}')
    for source in sorted((root / 'assets').glob('*.svg')):
        try:
            ET.parse(source)
        except ET.ParseError as error:
            errors.append(f'{source.relative_to(root)}: invalid SVG: {error}')
    return errors

if __name__ == '__main__':
    errors = check(Path(__file__).resolve().parents[1])
    print('\n'.join(errors) if errors else 'Local links and SVG assets are valid.')
    sys.exit(bool(errors))
