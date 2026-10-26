# Troubleshooting HrishikeshLenin13

Use the smallest reproducible fixture before changing production data or configuration. Run commands from the repository root.

## A heading fragment fails

Compare the fragment with the normalized heading slug and its duplicate suffix. Preserve heading anchors when editing public sections.

## A directory link fails

Create a README.md in the target directory or link to the intended file explicitly.

## A reference link fails

Define its label in the same Markdown file; code examples do not define real links.

## Reproduce and report

1. Record the exact command or UI action, runtime version, expected result, and actual result.
2. Run the regression command below on the same checkout and keep its first failure, not only the final summary.
3. Reduce the issue to a deterministic fixture without personal data or credentials.
4. Include the affected source path from the [feature guide](RECENT_IMPROVEMENTS.md) and whether it reproduces on a clean checkout.

```sh
python3 scripts/check_links.py && python3 -m unittest discover -s tests -v
```

## Recovery

Keep a copy of input data before experimenting. Revert the individual source change with Git and rerun the same fixture; a source revert does not automatically reverse browser storage, downloaded files, or external service state. Do not delete a lockfile or weaken a validation gate to make a failure disappear.
