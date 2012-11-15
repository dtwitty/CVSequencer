import sys
import cv2
import numpy as np
import SocketServer
import json
import threading
from utils import *

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        if data:
            dic = json.loads(data)
            level = dic['level']
            threshold = dic['threshold']
            inv = dic['invert']
            to_send = read_frame(src, level, threshold, inv)
            self.request.send(json.dumps(to_send))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
        
    
cap = cv2.VideoCapture(0)
(un, src) = cap.read()
to_send = {}
if __name__ == '__main__':
    host = ''
    port = 50000
    server = ThreadedTCPServer((host,port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    while(1):
        (un, src) = cap.read()




    
    


