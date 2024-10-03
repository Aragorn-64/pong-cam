from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import base64
import numpy as np
import cv2
import datetime

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rtc')
def index_rtc():
    return render_template('index-rtc.html')


@socketio.on('video_stream')
def handle_video_stream(message):
    # Decode the base64 image from the message
    image_data = message.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)

    # Convert the image to a format usable by OpenCV
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    emit('recv')

    save_frame(image)


def save_frame(frame):
    curr = datetime.datetime.now()
    cv2.imwrite(f'./frames/{curr}.jpg', frame)


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=5000,
    #              ssl_context=('cert.pem', 'key.pem'))
    socketio.run(app, host='0.0.0.0', port=5000)
