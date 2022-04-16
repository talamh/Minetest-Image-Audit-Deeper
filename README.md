# Minetest-Image-Audit-Deeper

WIP: No actual auditing implemented yet.

currently only downloads the jar files we will need, and indexes the contained
image files into groups based on size.

edit the list "check_against" in audit_deeper.py main() to select
versions of interest, it only downloads version 1.8.9 by default

list of all jars that can be downloaded is in the file available_jars.txt

## requirements
requests

```bash
$ pip install requests
```

PILLOW

```bash
$ pip install PILLOW
```
