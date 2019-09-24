import os
from flask import Blueprint, request, redirect
from werkzeug.utils import secure_filename


upload_file = Blueprint('upload_file', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = (os.path.realpath('.') + '/images/')


def allowed_file(filename):
    """ @summary A function to check for a valid file extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload_file.route("/upload", methods=['GET', 'POST'])
def upload():
    """ @summary A function to handle a file upload
    """
    if request.method == 'POST':
        print("saving file")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        return redirect('/')
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(UPLOAD_FOLDER,))


def upload_from_another_form(file):
    """ @summary A function to handle a file upload from within another main form
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
