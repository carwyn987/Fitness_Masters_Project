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
    # if 'image' not in request.files:
    #     return 'No image file provided', 400
    # print("!!!!!!!!!!!!!!!!")

    # # get the file from the request and save it to disk
    # file = request.files['image']
    # file.save('image.png')

    file = request.files['image']
    print("TYPE OF FILE: ", type(file))
    # file.save('abcd3.jpeg')

    # Get image from BytesIO
    in_memory_file = io.BytesIO()
    file.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)

    # Blur image
    kernel = np.ones((10,10),np.float32)/100
    img = cv2.filter2D(img,-1,kernel)
    img = cv2.imread('abcd3.png')
    # img[100:200, 100:200, :] = 1

    # Get BytesIO from image
    ret, data = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90]) # ret is if the operation was successful
    print("Was the encoding data operation successful?: ", ret)
    d = data.tostring() # back to bytes
    # d = io.BytesIO(data).getvalue() #.decode("utf-8")
    # d = str(np.array(data).tobytes())
    print(d)

    # return a response to indicate success
    # return 'Image file uploaded successfully', 200
    r = Response(response=d,
                    status=200,
                    mimetype="application/json")
    r.data = d
    return r


if __name__ == '__main__':
    app.run()