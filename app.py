
from flask import Flask, request, flash, redirect, url_for
from flask.templating import render_template
from model import get_prediction
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

app.secret_key = "pelican"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def uploadImage():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if request.form['submit_button'] == 'predict':
            file = request.files['file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('Image successfully uploaded and displayed below')
                with open("./static/uploads/%s" % filename, "rb") as image:
                    img_bytes = image.read()
                    _, class_name = get_prediction(image_bytes=img_bytes)
                    prediction = class_name
                return render_template('index.html', filename=filename, prediction=prediction)
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
