# client.py
import os
import requests

def get_secret_message():
    os.environ["SECRET_URL"] = "http://127.0.0.1:5683/"
    url = os.environ["SECRET_URL"]
    response = requests.get(url)
    print(f"The secret message is: {response.text}")

if __name__ == "__main__":
    get_secret_message()