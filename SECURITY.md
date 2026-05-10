# Security Policy

## Supported versions

Only the most recent commit on `main` is supported. Older versions do not receive security fixes.

## Reporting a vulnerability

Please **do not** open a public issue for security problems.

Instead, use GitHub's private vulnerability reporting:
<https://github.com/thiagobra/Resize-all-Images-in-a-folder/security/advisories/new>

You should receive an acknowledgement within 7 days. If the report is confirmed, a fix will land on `main` and a brief advisory will be published.

## Scope

This project depends on [Pillow](https://pillow.readthedocs.io/), which has a history of CVEs in image-parsing code paths. If you find a vulnerability that originates in Pillow itself, please report it upstream as well: <https://github.com/python-pillow/Pillow/security>.
