# Epigenome switchboard UI

A simple Flask web application to interact with the [episb-rest-server](https://github.com/databio/episb/tree/master/episb-rest-server)

## Search

Current functionality is to search by START and STOP values. Results can be searched by hand from the home page episb.org or passed as URL parameters:

    http://episb.org/segment/54321/500000

JSON results can also be retrieved, add `/json/` to the endpoint:

    http://episb.org/segment/json/54321/500000

Additional queries will be added in the near future.
