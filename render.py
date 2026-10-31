#!/usr/bin/env python3
"""Render the Journali legal Markdown into standalone HTML pages.

Source of truth is the private `journali` repo (docs/privacy-policy.md and
docs/terms.md). Run this from the `journali-legal` checkout, pointing at that
repo:

    python render.py /path/to/journali/docs

Writes privacy-policy.html and terms.html next to this script.
"""

import pathlib
import sys

import markdown

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Journali</title>
<meta name="description" content="{title} for Journali, a language-learning journaling app for iOS.">
<style>
  :root {{
    color-scheme: light dark;
    --fg: #1c1c1e;
    --muted: #6c6c70;
    --bg: #ffffff;
    --rule: #e5e5ea;
    --link: #c2185b;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --fg: #f2f2f7; --muted: #aeaeb2; --bg: #000000; --rule: #2c2c2e; --link: #ff6b9d; }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--fg);
    font: 17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    -webkit-text-size-adjust: 100%;
  }}
  main {{ max-width: 42rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }}
  h1 {{ font-size: 2rem; line-height: 1.2; letter-spacing: -0.02em; margin: 0 0 0.5rem; }}
  h2 {{ font-size: 1.25rem; margin: 2.5rem 0 0.75rem; }}
  h3 {{ font-size: 1.05rem; margin: 1.75rem 0 0.5rem; }}
  p, li {{ margin: 0.75rem 0; }}
  ul, ol {{ padding-left: 1.4rem; }}
  a {{ color: var(--link); }}
  hr {{ border: 0; border-top: 1px solid var(--rule); margin: 2.5rem 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; display: block; overflow-x: auto; }}
  th, td {{ border: 1px solid var(--rule); padding: 0.5rem 0.7rem; text-align: left; vertical-align: top; }}
  th {{ background: rgba(128,128,128,0.08); }}
  code {{ font-size: 0.9em; background: rgba(128,128,128,0.12); padding: 0.1em 0.35em; border-radius: 4px; }}
  blockquote {{ margin: 1rem 0; padding-left: 1rem; border-left: 3px solid var(--rule); color: var(--muted); }}
  em {{ color: var(--muted); }}
  footer {{ margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--rule); font-size: 0.85rem; color: var(--muted); }}
  footer a {{ color: var(--muted); }}
</style>
</head>
<body>
<main>
{body}
<footer>
  <p>Journali is an open-source iOS app. <a href="https://github.com/Chris-Mooney852/journali">Source repository</a> &middot; <a href="{sibling}">{sibling_title}</a></p>
</footer>
</main>
</body>
</html>
"""

# Markdown files whose trailing repo-internal notes must not be published.
INTERNAL_NOTE_MARKERS = (
    "*This policy is published from",
)

PAGES = [
    {
        "source": "privacy-policy.md",
        "output": "privacy-policy.html",
        "title": "Privacy Policy",
        "sibling": "terms.html",
        "sibling_title": "Terms of Use",
    },
    {
        "source": "terms.md",
        "output": "terms.html",
        "title": "Terms of Use",
        "sibling": "privacy-policy.html",
        "sibling_title": "Privacy Policy",
    },
]


def strip_internal_notes(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(INTERNAL_NOTE_MARKERS):
            return "\n".join(lines[:index]).rstrip() + "\n"
    return text


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    source_dir = pathlib.Path(sys.argv[1])
    out_dir = pathlib.Path(__file__).parent

    for page in PAGES:
        source = source_dir / page["source"]
        if not source.exists():
            print(f"missing source: {source}")
            return 1
        text = strip_internal_notes(source.read_text(encoding="utf-8"))
        body = markdown.markdown(
            text,
            extensions=["tables", "fenced_code", "sane_lists"],
            output_format="html5",
        )
        html = PAGE.format(
            title=page["title"],
            body=body,
            sibling=page["sibling"],
            sibling_title=page["sibling_title"],
        )
        target = out_dir / page["output"]
        target.write_text(html, encoding="utf-8")
        print(f"wrote {target.name} ({len(html)} bytes)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
