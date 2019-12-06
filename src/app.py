import os
import cv2
from flask import Flask, request, render_template, send_from_directory
import numpy as np

__author__ = 'hello.com'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def model_detect(frame):
    return [frame, frame, frame, frame, frame]


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():

    frame_list = []
    file_objects = []
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for file_upload in request.files.getlist("file"):
        print(file_upload)
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
            frame_list.append(fr)
            d = {"name": i, "num": 0.11}
            file_objects.append(d)
            i += 1
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file_upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("gallery.html", image_names=[filename])


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/gallery')
def get_gallery():
    image_names = os.listdir('./images')
    print(image_names)
    return render_template("gallery.html", image_names=image_names)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
