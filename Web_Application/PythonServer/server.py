from flask import Flask, request, Response
import io
import numpy as np
import cv2
import base64

from process import processMain

app = Flask(__name__, static_folder='public', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')


def loadImg(imgName):
    file1 = request.files[imgName]
    
    # Get image from BytesIO
    in_memory_file = io.BytesIO()
    file1.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    return img

@app.route('/upload-image', methods=['POST'])
def upload_image():
    print(request.files)
    # check if the request contains a file
    if 'image' not in request.files:
        return 'No image file provided', 400

    img1 = loadImg('image')
    img2 = loadImg('image2')
    t_img1 = loadImg('t_img1')
    t_img2 = loadImg('t_img2')

    # processing
    img = processMain(img1, img2, t_img1, t_img2)

    # Get encoding
    retval, buffer = cv2.imencode('.jpg', img)
    if not retval: print("The image encoding failed!")
    jpg_as_text = base64.b64encode(buffer)

    # return a response to indicate success
    # return 'Image file uploaded successfully', 200
    return Response(response=jpg_as_text,
                    status=200)

if __name__ == '__main__':
    app.run()