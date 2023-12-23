import queue
from flask import Flask, Response,render_template,request
import json
import cv2
import numpy as np
import base64
import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
#from flask_sslify import SSLify

app = Flask(__name__)
#sslify = SSLify(app)





#######################################################################
#######################################################################

#default route
@app.route('/')
def home():
    return render_template('./index.html')
#######################################################################

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        self.listeners.append(queue.Queue(maxsize=5))
        return self.listeners[-1]

    def announce(self, msg):
        # We go in reverse order because we might have to delete an element, which will shift the
        # indices backward
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


announcer = MessageAnnouncer()

#######################################################################

class DoorLockStatus:
    def __init__(self) -> None:
        self.doorStatus:str='open'
        self.lockStatus:str='unlocked'
    def getDoorStatus(self)->str:
        return self.doorStatus
    def getLockStatus(self)->str:
        return self.lockStatus
    def setDoorStatus(self,doorStatus)->None:
        self.doorStatus=doorStatus
    def setLockStatus(self,lockStatus)->None:
        self.lockStatus=lockStatus

dlstatus=DoorLockStatus()

#######################################################################

class DetectionStats:
    def __init__(self) -> None:
        self.humanNumber:int=0;
        self.NotifyFlag:bool=False;
    def getHumanNumber(se)->str:
        return self.humanNumber
    def setHumanNumber(self,numberOfHumans)->None:
        self.humanNumber=numberOfHumans

detStats=DetectionStats()
#######################################################################
def format_sse(data:any, event=None,type:str='json') -> str:
    """
        default datatype is a dictionary that gets converted to a json string 
        but a text can also be passed  
    """
    extendedData={
        "img":data,
        "lock":dlstatus.getLockStatus(),
        "door":dlstatus.getDoorStatus()
    }

    if type=='json':
        msg = f'data: {json.dumps(extendedData)}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
            return msg
    else:
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
            return msg
        
#######################################################################   
         
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detectPerson(inImg):
    
    imgBytesIn = base64.b64decode(inImg)
    imgArrIn = np.frombuffer(imgBytesIn, dtype=np.uint8)  
    image = cv2.imdecode(imgArrIn, flags=cv2.IMREAD_COLOR)
    (humans, _) = hog.detectMultiScale(image, winStride=(10, 10),padding=(32, 32), scale=1.1)

    # getting no. of human detected
    #print('Human Detected : ', len(humans))
    detStats.setHumanNumber(len(humans))

    # loop over all detected humans
    for (x, y, w, h) in humans:
        pad_w, pad_h = int(0.15 * w), int(0.01 * h)
        cv2.rectangle(image, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)

    _, imgArr = cv2.imencode('.jpg', image)  # im_arr: image in Numpy one-dim array format.
    imgData= base64.b64encode(imgArr).decode('ascii')
    return imgData


#######################################################################
@app.route('/img_in',methods=['post'])
def img_in():
    data:dict = json.loads(request.get_json())

    processedImg=   data['img']
    
    data_out = format_sse(data=processedImg,event="frame")
    announcer.announce(msg=data_out)

    return {"responseStatus":"ok",
            "responseHeader":{
            "status":"ok",
             }}, 200

#######################################################################

@app.route('/sensor_data',methods=['post'])
def sensor_data():
    data = request.get_json()
    if data.keys() >= {"lock", "door"}:
            dlstatus.setDoorStatus(data.door)
            dlstatus.setLockStatus(data.lock)

    return {"responseStatus":"ok",
            "responseHeader":{
            "status":"ok",
             }}, 200

#######################################################################

@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')
#######################################################################

if __name__ == '__main__':
    #app.run(ssl_context='adhoc')
    app.run()
    
