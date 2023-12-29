import json
import requests
import base64
from picamera import PiCamera
import numpy as np
import cv2
import io

# Initialize PiCamera
camera = PiCamera()

def im2json(im):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, imdata = cv2.imencode(".jpg", im, encode_param)
    jstr = json.dumps({"img": base64.b64encode(imdata).decode('ascii')})
    return jstr

def get_img():
    # Capture image from the Raspberry Pi camera
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data, 1)
    return im2json(img)

def postImg():
    while True:
        imgjson = get_img()
        try:
            requests.post('http://localhost:7777/img_in', json=imgjson, timeout=0.1)
        except requests.exceptions.ReadTimeout:
            pass

if __name__ == '__main__':
    postImg()
