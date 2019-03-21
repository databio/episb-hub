# How to build a hub


To build the episb-hub container locally and test, follow these steps:

### 1. Clone the [episb-hub](https://github.com/databio/episb-hub) repository.

```console
git clone git@github.com:databio/episb-hub.git
```

### 2. `cd` in and build the docker image from the `Dockerfile`:

```console
cd episb-hub
docker build -t episb-hub .
```

### 3. Run the container from the image you just built:

```console
docker run -d -p 80:80 --rm --name episb-hub episb-hub
```

### 4. Interact with and preview the site

Visit: http://localhost/ 

### 5. When done, stop the container:

```console
docker stop episb-hub
```
