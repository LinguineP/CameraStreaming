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
    #return im2json(frame)
    return im2json(frame)



def postImg():
     while True:     
        #a=time.time()
        imgjson=get_img();
        #print(imgjson)

       # b=time.time();
        try:
            requests.post('http://localhost:7777/img_in',json=imgjson,timeout=0.1)
        except requests.exceptions.ReadTimeout: 
            pass
        
        #print(b-a)
        

if __name__ == '__main__':
    
    postImg()
   