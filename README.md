# Episb hub

User documentation can be found at http://databio.org/episb

## Running the app for development

```
FLASK_APP="main.py" flask run
```

Point browser to http://localhost:5000/


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

### Running the app in a container with development mode

To run the container and have it reflect the changes, use the Dockerfile_dev to build the image:

```
docker build -f Dockerfile_dev -t <docker image>:<tag optional> .
```

To run the container:

```
$ docker run -v /path/to/host/episb-hub:/app -p 80:80 --rm --name episb-hub -e FLASK_APP=main.py -e FLASK_DEBUG=1 episb flask run --host=0.0.0.0 --port=80
```

Now the development container will be viewable on your `localhost` and update with any changes you make.

### Configuration

Starting with release 0.3, setting variables in a configuration file named 'episb-hub.cfg' is required.

The file has the following sections/variables:

```
[Providers]
DefaultProvider=<URL of the data provider used to serve data to the hub> (e.g. http://provider.episb.org/episb-provider)

[HubServer]
ServerHost=<URL of the host the hub is running on> (e.g. http://episb.org)
ServerPort=<port the app is running on> (e.g. 8080)
```

### Data provider

Episb-hub depends on the APIs served to it by a [data provider](https://github.com/databio/episb-provider/tree/master/episb-provider)

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
