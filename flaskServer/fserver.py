import queue
from flask import Flask, Response,render_template,request,jsonify
import json
import cv2
import numpy as np
import base64
import logging
import pkg_resources
from flask_cors import CORS
import concurrent.futures
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
#from flask_sslify import SSLify

app = Flask(__name__)
#sslify = SSLify(app)
CORS(app)



######################################################################
server_host:str=''
#######################################################################
#######################################################################

def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text_content = file.read()
        return text_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None



########################################################################

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # Use 465 for SSL
        self.smtp_username = "helloWorldFromSrv@gmail.com"
        self.file_path = './pass.txt'  # Replace with the actual file path
        self.file_content = read_text_from_file(self.file_path)
        self.smtp_password = 'seuq utdl niuv aqlu'
        self.serverIP=None

        
        # Initialize email details
        self.subject_lock = "Forgot to lock door!!"
        self.body_lock = "go look at the camera feed on http://" +self.serverIP
        self.to_email = "vpavle021@gmail.com"

    def set_to_email(self,to_email):
        self.to_email = to_email
    def setSrvIp(self,ip):
        self.serverIP=ip

    def send_email_Lock(self):
        # Create the email message
        message = MIMEMultipart()
        message['From'] = self.smtp_username
        message['To'] = self.to_email
        message['Subject'] = self.subject_lock

        # Attach the email body as plain text
        message.attach(MIMEText(self.body_lock, 'plain'))

        # Connect to the SMTP server
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            # Login to the email account
            server.starttls()  # Use this line if your SMTP server requires a secure connection
            server.login(self.smtp_username, self.smtp_password)

            # Send the email
            server.sendmail(self.smtp_username, self.to_email, message.as_string())
#########################################################################
emailSndr=EmailSender(ip=request.host)



#default route
@app.route('/')
def home():
    return render_template('./index.html')
#######################################################################
@app.route('/change_email')
def change_email():
    data=request.get_json()
    if data['auth']=='deadbeef':
        emailSndr.set_to_email(data['email'])

    return {"responseStatus":"ok",
            "responseHeader":{
            "status":"ok"
             }}, 200


@app.route('/send_email')
def send_email():
    emailSndr.setSrvIp(request.host)
    logging.getLogger().debug(f"{request.host}")
    emailSndr.send_email_Lock()
    return {"responseStatus":"ok",
            "responseHeader":{
            "status":"ok"
             }}, 200
    

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
        self.presentHumans:bool=False;
        self.NotifyFlag:bool=False;
        self.doDetectionFlag:bool=False;
    def getHumanPresent(self)->bool:
        return self.presentHumans
    def setHumanPresent(self,presentHumans)->None:
        self.presentHumans=presentHumans
    def getNotify(self)->bool:
        return self.presentHumans
    def setNotify(self,presentHumans)->None:
        self.presentHumans=presentHumans
    def getDetect(self)->bool:
        return self.doDetectionFlag
    def setDetect(self,detect)->None:
        self.doDetectionFlag=detect



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
         

upperbody_xml = pkg_resources.resource_filename(
    'cv2', 'data/haarcascade_upperbody.xml')         
upperBody_cascade = cv2.CascadeClassifier(upperbody_xml) 
#___________________________________________________________
profileface_xml = pkg_resources.resource_filename(
    'cv2', 'data/haarcascade_profileface.xml')         
profileFace_cascade = cv2.CascadeClassifier(profileface_xml) 
#___________________________________________________________
frontalface_xml = pkg_resources.resource_filename(
    'cv2', 'data/haarcascade_frontalcatface_extended.xml')         
frontalFace_cascade = cv2.CascadeClassifier(profileface_xml) 

cascadeList=[upperBody_cascade,frontalFace_cascade,profileFace_cascade]
   

def CascadeClassify(classifier,img):
    arrUpperBody = classifier.detectMultiScale(img)
  
    for (x,y,w,h) in arrUpperBody:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        if (w*h)!=0:
            detStats.setHumanPresent(True)
    return img

def detect_human(cascade, img):
    result = CascadeClassify(cascade, img)
    return result, detStats.getHumanPresent()


def detect(inImg):
    
    imgBytesIn = base64.b64decode(inImg)
    imgArrIn = np.frombuffer(imgBytesIn, dtype=np.uint8)  
    img = cv2.imdecode(imgArrIn, flags=cv2.IMREAD_COLOR)
    detStats.setHumanPresent(False)

    """for cascade in cascadeList:
        img=CascadeClassify(cascade,img)
        if detStats.getHumanPresent():
            break"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Schedule the detection tasks in parallel
        detection_tasks = {executor.submit(detect_human, cascade, img): cascade for cascade in cascadeList}

        # Wait for all tasks to complete
        for future in concurrent.futures.as_completed(detection_tasks):
            cascade = detection_tasks[future]
            try:
                result, human_present = future.result()
                if human_present:
                    print(f"Human detected using cascade: {cascade}")
                    break  # Exit the loop if a human is detected
            except Exception as e:
                print(f"Error processing cascade {cascade}: {e}")

    
        

    _, imgArr = cv2.imencode('.jpg', result)  
    imgData= base64.b64encode(imgArr).decode('ascii')
    return imgData


#######################################################################
skip1=False;

@app.route('/img_in',methods=['post'])
def img_in():
    data:dict = json.loads(request.get_json())
    global skip1
    if detStats.getDetect():
        if skip1:
            processedImg= detect(data['img']);    
        else:
            processedImg= data['img'];    
        
        skip1=not skip1
    else:
        processedImg= data['img'];
        
    
    
    data_out = format_sse(data=processedImg,event="frame")
    announcer.announce(msg=data_out)

    return {"responseStatus":"ok",
            "responseHeader":{
            "status":"ok"
             }}, 200

#######################################################################

@app.route('/settings',methods=['GET','PUT'])
def settings():
    
    if request.method == 'PUT':
        
        data=request.get_json()
        
        if 'detect' in data:
            detStats.setDetect(data['detect'])
        if 'notify' in data:
            detStats.setNotify(data['notify'])
        data = {
            "detection": detStats.getDetect(),
            "notify": detStats.getNotify()
        }
        response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
        )
        return response

    if request.method == 'GET':
        data = {
            "detection": detStats.getDetect(),
            "notify": detStats.getNotify()
        }
        response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
        )
        return response
    response = jsonify({'status': 404,'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response




@app.route('/sensor_data',methods=['POST'])
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
    app.run(host='localhost', port=7777)
    #app.run(host='0.0.0.0', port=7777)
    
