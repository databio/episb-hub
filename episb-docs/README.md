These docs can be rendered locally for development with:

```
mkdocs serve -f mkdocs.yml
```

And can be built for deploy with:

```
RENDERED_DIR="$CODEBASE/code.databio.org/episb"
mkdocs build -f episb-docs/mkdocs.yml -d "$RENDERED_DIR"
```

Or by running `update_docs.sh`.
