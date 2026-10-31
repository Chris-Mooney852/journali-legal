# Journali — legal pages

Public hosting for the privacy policy and terms of use of the
[Journali](https://github.com/Chris-Mooney852/journali) iOS app.

- [Privacy Policy](privacy-policy.html)
- [Terms of Use](terms.html)

These pages are served by GitHub Pages from this repository. It intentionally
contains **only** the two documents — no app source code.

## Updating

The Markdown sources live in the private `journali` repository
(`docs/privacy-policy.md`, `docs/terms.md`) and are the single source of truth.
To publish a change:

```sh
python3 -m venv .venv && ./.venv/bin/pip install markdown
./.venv/bin/python render.py ../journali/docs
git commit -am "Update legal pages" && git push
```

Update both the `Last updated` date in the Markdown and the version published
here in the same change.
