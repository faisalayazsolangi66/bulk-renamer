# Bulk Renamer

Rename many files at once with a pattern, prefix, or numbering.

## Requirements

- Python 3.8+
- No third-party packages (standard library only)

## Usage

```bash
python3 main.py <folder> [--pattern PATTERN] [--prefix TEXT] [--suffix TEXT]
                          [--start N] [--extension .jpg] [--dry-run] [--recursive]
```

Pattern placeholders: `{n}` (number), `{n:03d}` (zero-padded number), `{name}` (original stem), `{ext}` (original extension).

## Example

```bash
$ python3 main.py ./photos --pattern "photo_{n:03d}" --dry-run
[dry-run] a.jpg -> photo_001.jpg
[dry-run] b.jpg -> photo_002.jpg
Done. 2 file(s) considered.
```

## License

MIT — see [LICENSE](LICENSE).
