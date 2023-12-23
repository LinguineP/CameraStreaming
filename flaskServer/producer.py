import time
import cv2
import json
import requests
import base64
captureDev=cv2.VideoCapture(0);


def im2json(im):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, imdata = cv2.imencode(".jpg",im,encode_param)
    jstr = json.dumps({"img": base64.b64encode(imdata).decode('ascii')})
    return jstr

def get_img():
    ret, frame = captureDev.read()    
    return im2json(frame)


if __name__ == '__main__':
    while True:     
        a=time.time()
        imgjson=get_img();
        #print(imgjson)
        b=time.time();
        requests.post('http://localhost:5000/data_in',json =imgjson)
        
        print(b-a)
        time.sleep(0.05)
        
