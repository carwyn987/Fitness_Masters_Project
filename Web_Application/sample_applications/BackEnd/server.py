from flask import Flask
from flask_cors import CORS

SECRET_MESSAGE = "fluffy tail"
app = Flask(__name__)
CORS(app)

@app.route("/")
def get_secret_message():
    return SECRET_MESSAGE

@app.route("/gaussian")
def get_gaussian_blur(image):
    print("GOT GAUSSIAN !!!!!")
    return image

'''
To make this work with a separate web server (i.e. the one in web_client), I needed to turn of CORS so that the cross-domain request would pass.
To achieve this, I added the "from flask_cors import CORS" and "CORS(app)" lines.

A user from where I got this solution:
https://stackoverflow.com/questions/20035101/why-does-my-javascript-code-receive-a-no-access-control-allow-origin-header-i 
wrote this:
"You shouldn't turn off CORS because you don't know what its for. This leaves your users in a fundamentally unsafe state."

For the final production server, make sure to remove this.
'''