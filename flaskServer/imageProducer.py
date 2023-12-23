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


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detectPerson(inImg):
    
    
    (humans, _) = hog.detectMultiScale(inImg, winStride=(10, 10),padding=(32, 32), scale=1.1)

    # getting no. of human detected
    print('Human Detected : ', len(humans))


    # loop over all detected humans
    for (x, y, w, h) in humans:
        pad_w, pad_h = int(0.15 * w), int(0.01 * h)
        cv2.rectangle(inImg, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)

    _, imgArr = cv2.imencode('.jpg', inImg)  # im_arr: image in Numpy one-dim array format.
    jstr = json.dumps({"img": base64.b64encode(imgArr).decode('ascii')})
    return jstr


def get_img():
    ret, frame = captureDev.read()    
    #return im2json(frame)
    return detectPerson(frame)



def postImg():
     while True:     
        #a=time.time()
        imgjson=get_img();
        #print(imgjson)

       # b=time.time();
        try:
            requests.post('http://localhost:5000/img_in',json=imgjson,timeout=0.1)
        except requests.exceptions.ReadTimeout: 
            pass
        
        #print(b-a)
        

if __name__ == '__main__':
    
    postImg()
   