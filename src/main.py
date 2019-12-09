import os
from io import BytesIO
import io
from PIL import Image
import numpy as np
import cv2
import uuid

from flask import Flask, request, render_template, send_from_directory, send_file

__author__ = 'hello.com'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

images_list = {}
frame_list = {}


def model_detect(frame):
    return [frame, frame, frame, frame, frame]


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    global frame_list

    file_objects = []

    print("req file: ", request.files.getlist("file"))
    for file_upload in request.files.getlist("file"):
        print("file_upload: ", file_upload)
        print("{} is the file name".format(file_upload.filename))
        filename = file_upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files file_uploaded are not supported...")

        # read image file string data
        filestr = file_upload.read()
        # convert string data to  frame (numpy array)
        npimg = np.frombuffer(filestr, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert BGR back to RGB,

        # TODO: MODEL
        frames = model_detect(frame)

        for fr in frames:
            image_id = uuid.uuid4()
            frame_list[str(image_id)] = fr
            d = {"id": image_id, "num": 0.11}
            file_objects.append(d)

    return render_template("gallery.html", image_names=file_objects)


@app.route('/upload/<filename>')
def send_image(filename):
    global frame_list
    # convert numpy array to PIL Image
    image_id = filename

    img = Image.fromarray(frame_list[image_id].astype('uint8'))
    del frame_list[image_id]

    # create file-object in memory
    file_object = io.BytesIO()

    # write PNG in file-object
    img.save(file_object, 'PNG')

    # move to beginning of file so `send_file()` it will read from start
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')


if __name__ == "__main__":
    app.run(port=8000, debug=True)
