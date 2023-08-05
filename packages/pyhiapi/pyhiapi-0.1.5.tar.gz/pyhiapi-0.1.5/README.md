# pyhiapi

The API that just says hi!

A very simple API endpoint, easily deployable for testing purposes.

## Installation

    sudo pip install pyhiapi

## Usage

		hiapi [-h] [-b BIND] [-p PORT] [-c CODE]
		
		optional arguments:
		  -b BIND, --bind-address BIND
		  -p PORT, --port PORT
		  -c CODE, --response_code CODE

hiapi defaults to `localhost:4000` and a `200 OK` response.

## Testing

You can just curl the service, perhaps like this:

    $ curl -i http://localhost:4000/

    HTTP/1.0 200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 4
    Server: Werkzeug/0.9.6 Python/2.7.8
    Date: Fri, 23 Jan 2015 03:38:14 GMT

    Hi!

