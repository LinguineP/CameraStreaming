import queue

from flask import Flask, Response,render_template,request
import time
import cv2
import json


app = Flask(__name__)

#default route
@app.route('/')
def home():
    return render_template('./index.html')


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


def format_sse(data:any, event=None,type:str='json') -> str:
    """Formats a string and an event name in order to follow the event stream convention.

    >>> format_sse(data=json.dumps({'abc': 123}), event='Jackson 5')
    'event: Jackson 5\\ndata: {"abc": 123}\\n\\n'

    """
    

    msg = f'data: {json.dumps(data)}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg




@app.route('/data_in',methods=['post'])
def data_in():
    data = request.get_json()
    #print(data)
    data_out = format_sse(data=data,event="frame")
    announcer.announce(msg=data_out)
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
    
