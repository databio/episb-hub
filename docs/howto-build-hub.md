# How to build a hub

To build the episb-hub container locally and test, follow these steps:

- Clone the episb-hub repository.
```
git clone git@github.com:databio/episb-hub.git
```

- cd in and build the docker image from the Dockerfile:
```
cd episb-hub
docker build -t episb-hub .
```

- Run the container from the image you just built:
```
docker run -d -p 80:80 --rm --name episb-hub episb-hub
```
- Interact with and preview the site

Visit: http://localhost/

- When done, stop the container:
```
docker stop episb-hub
```
