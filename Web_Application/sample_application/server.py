from flask import Flask

SECRET_MESSAGE = "fluffy tail"
app = Flask(__name__)

@app.route("/")
def get_secret_message():
    return SECRET_MESSAGE

'''
Using the command uwsgi --http-socket 127.0.0.1:5683 --mount /=server:app
You can view the "secret message at http://localhost:5683/

uwsgi - starts up a web server with a single process and a single thread.
'''