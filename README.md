# Episb hub

Use documentation can be found at http://databio.org/episb

## Running the app for development

```
FLASK_APP="main.py" flask run
```

Point browser to http://localhost:5000


## Running the app in a container

To build the episb-hub container locally and test, follow these steps:

1. In the same directory as the `Dockerfile`:

```
$ docker build -t <docker image>:<tag optional> .
```

2. Run the container from the image you just built:

```
$ docker run -d -p 80:80 --rm --name episb-hub <docker image>:<tag>
```

3. Interact with and preview the site: http://localhost/ 

4. When done, stop the container:

```
$ docker stop episb-hub
```


## Docs:

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
