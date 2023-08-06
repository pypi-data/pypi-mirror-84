"""Main module."""

from __future__ import division
import io
import json
import picamera
import picamera.array
import logging
import time
import socketserver
from threading import Condition
from http import server
import numpy as np

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/stream.mjpg':
    
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                time.sleep(1)

                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        elif self.path == "/framerate":
            self.send_response(200)
            self.end_headers()
            framerate = bytes(json.dumps({'framerate':int(camera.framerate)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(framerate)

        elif self.path == "/brightness":
            self.send_response(200)
            self.end_headers()
            brightness = bytes(json.dumps({'brightness':int(camera.brightness)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(brightness)

        elif self.path == "/contrast":
            self.send_response(200)
            self.end_headers()
            contrast = bytes(json.dumps({'contrast':int(camera.contrast)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(contrast)

        elif self.path == "/saturation":
            self.send_response(200)
            self.end_headers()
            saturation = bytes(json.dumps({'saturation':int(camera.saturation)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(saturation)

        elif self.path == "/sharpness":
            self.send_response(200)
            self.end_headers()
            sharpness = bytes(json.dumps({'sharpness':int(camera.sharpness)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(sharpness)
        
        elif self.path == "/exposure":
            self.send_response(200)
            self.end_headers()
            exposure = bytes(json.dumps({'exposure':str(camera.exposure_mode)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(exposure)

        elif self.path == "/effect":
            self.send_response(200)
            self.end_headers()
            effect = bytes(json.dumps({'effect':str(camera.image_effect)}, ensure_ascii=False), 'utf-8')
            self.wfile.write(effect)

        

        # elif self.path == "/motion":
        #     self.send_response(200)
        #     self.send_header('Age', 0)
        #     self.send_header('Cache-Control', 'no-cache, private')
        #     self.send_header('Pragma', 'no-cache')
        #     self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')            
        #     self.end_headers()
        #     try:
        #         while True:
        #             data = bytes(json.dumps({'motionDetected':motionDetected}, ensure_ascii=False), 'utf-8')
        #             self.wfile.write(b'--FRAME\r\n')
        #             self.send_header('Content-Type', 'text/html')
        #             self.send_header('Content-Length', len(data))

        #             self.end_headers()
        #             response = io.BytesIO()
        #             response.write(data)
        #             self.wfile.write(response.getvalue())
        #             self.wfile.write(b'\r\n')

        #     except Exception as e:
        #         logging.warning(str(e))

        elif self.path == "/capture":
            with output.condition:
                output.condition.wait()
                frame = output.frame
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers() 

            self.wfile.write(b'--FRAME\r\n')
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', len(frame))
            self.end_headers()
            self.wfile.write(frame)
            self.wfile.write(b'\r\n')

        elif self.path == "/rotate":
            
            self.send_response(200)
            self.end_headers()  

        elif self.path == "/resize":
            with output.condition:
                output.condition.wait()
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers() 

        else:
            self.send_error(404)
            self.end_headers()


    def do_POST(self):
        length = int(self.headers['content-length'])
        data = json.loads(self.rfile.read(length))

        if(self.path=="/resolution"):
            width = data['width']
            height = data['height']
            output.resolution = (640, 480)
            self.send_response(200)
            self.end_headers() 

        elif self.path=="/brightness":
            camera.brightness = int(data['brightness'])
            self.send_response(200)
            self.end_headers()

        elif self.path=="/sharpness":
            try:
                camera.sharpness = int(data['sharpness'])
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                logging.warning(e)
        
        elif self.path=="/contrast":
            camera.contrast = int(data['contrast'])
            self.send_response(200)
            self.end_headers()

        elif self.path=="/saturation":
            camera.saturation = int(data['saturation'])
            self.send_response(200)
            self.end_headers()

        elif self.path=="/exposure":
            camera.exposure_mode = str(data['exposure'])
            self.send_response(200)
            self.end_headers()

        elif self.path=="/effect":
            camera.image_effect = str(data['effect'])
            self.send_response(200)
            self.end_headers()

        elif self.path=="/framerate":
            camera.framerate = int(data['framerate'])
            self.send_response(200)
            self.end_headers()

        

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class MyMotionDetector(picamera.array.PiMotionAnalysis):
    
    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than 10 vectors with a magnitude greater
        # than 60, then say we've detected motion
        if (a > 60).sum() > 10:
            motionDetected = True
            print("Motion detected")
        else:
            motionDetected = False
def main():
    global camera
    with picamera.PiCamera() as camera:
        # motionDetected = False
        global output 
        output = StreamingOutput()
        camera.resolution=(640,480)
        camera.start_recording(output, format='mjpeg', splitter_port=1)
        with picamera.PiCameraCircularIO(camera, splitter_port=2, seconds=1):
            camera.start_recording("/dev/null", format='h264', splitter_port=2, motion_output=MyMotionDetector(camera))
        try:
            address = ('', 8000)
            server = StreamingServer(address, StreamingHandler)
            print("Server running on port 8000")
            server.serve_forever()
        finally:
            camera.stop_recording()

if __name__ == "__main__":
    main()
