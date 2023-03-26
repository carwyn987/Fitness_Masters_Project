# Flask Test Application

## Server Layout

Server uses Flask

For this test, it receives an image to the address / target:
http://127.0.0.1:5000/image

The image is altered via a gaussian blur (cv2).

The image is sent back via a HTTP response.

## Client Layout

Client takes an image from a user via a file input.

Sends a HTTP request to the backend Python server on a button click.

Receives an image in response which has a gaussian blur.

The image is finally showed on screen.