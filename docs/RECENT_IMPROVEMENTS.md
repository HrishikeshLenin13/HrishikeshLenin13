# Portable Markdown integrity checks

This guide covers implemented behavior. It does not change deployment or account configuration.

## Usage

```bash
python3 scripts/check_links.py
python3 scripts/check_links.py --root . --json
python3 -m unittest discover -s tests -v
```

## Contracts and limits

- The checker resolves repository-relative and repository-root paths, directory README targets, heading fragments, and reference-style links.
- Inline code and fenced code examples are excluded from link extraction. Duplicate heading slugs receive numeric suffixes.
- JSON diagnostics use an ok boolean and errors array. Broken links exit nonzero; a missing root is a usage error.
- This is a lightweight local Markdown checker, not a CommonMark renderer or an HTTP availability monitor. External destinations are not fetched.

## Source map

- [`scripts/check_links.py`](../scripts/check_links.py)
<!-- source: scripts/check_links.py -->
- [`tests/test_round2.py`](../tests/test_round2.py)
<!-- source: tests/test_round2.py -->

## Regression command

Run from the repository root:

```sh
python3 scripts/check_links.py && python3 -m unittest discover -s tests -v
```

