#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import Flask, render_template, jsonify, redirect, url_for, \
    request, send_from_directory, send_file
from convert import Convert

template_dir = os.path.abspath(os.path.join(os.getcwd(), "./templates"))
app = Flask(__name__,template_folder=template_dir )
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.getcwd(), "./data"))
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


@app.route("/home")
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    if request.method == 'POST':

        file = request.files['file']

        if not allowed_file(file.filename):

            return {"status":400, "msg":  "provided file type not supported. "
                                          "Expected pdf document as input"}

        if file and file.filename.endswith("pdf"):

            now = datetime.now()
            filename = os.path.join(app.config['UPLOAD_FOLDER'], "%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
            file.save(filename)
            converter  = Convert(filename)
            converter.extract_text()
            converter.convert_text()
            return_file = converter.create_pdf()

            return send_from_directory(directory=os.path.dirname(return_file),
                                       filename=os.path.basename(return_file),
                                       as_attachment=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)