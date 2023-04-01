from flask import Flask, request
app = Flask(__name__, static_folder='public', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    print(request.files)
    # check if the request contains a file
    # if 'image' not in request.files:
    #     return 'No image file provided', 400
    # print("!!!!!!!!!!!!!!!!")

    # # get the file from the request and save it to disk
    # file = request.files['image']
    # file.save('image.png')

    file = request.files['image']
    file.save('abcd3.jpeg')

    # return a response to indicate success
    return 'Image file uploaded successfully', 200

if __name__ == '__main__':
    app.run()