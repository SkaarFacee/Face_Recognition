from flask import Flask, render_template, request, flash, redirect
import os
from werkzeug.utils import secure_filename
sys.path.insert(1, './src/')
from predict import predict_img

app = Flask(__name__)

WORKING_DIRECTORY = './static/working-dir/'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)
            res=predict_img(img_path)
            return render_template('index.html', state=1, res=None)
    else:
        if os.listdir(WORKING_DIRECTORY) != []:
            for f in os.listdir(WORKING_DIRECTORY):
                if f != "temp.txt":
                    os.remove(os.path.join(WORKING_DIRECTORY, f))
    return render_template('index.html', state=0, res=None)

app.config['UPLOAD_FOLDER'] = WORKING_DIRECTORY
app.run(debug=True)