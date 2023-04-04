from flask import Flask, request, Response, send_file
import io
import numpy as np
import cv2

app = Flask(__name__, static_folder='public', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    print(request.files)
    # check if the request contains a file
    if 'image' not in request.files:
        return 'No image file provided', 400

    file = request.files['image']
    
    # Get image from BytesIO
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)

    # Blur image
    kernel = np.ones((10,10),np.float32)/100
    img = cv2.filter2D(img,-1,kernel)

    # return a response to indicate success
    return 'Image file uploaded successfully', 200

if __name__ == '__main__':
    app.run()