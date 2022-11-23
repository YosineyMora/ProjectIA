from flask import Flask, render_template, Response, request
from camera import VideoCamera
from reporte import generarReporte
from reportAllIn import generarAllReporte
from reportGroupAll import generarGroupAllReporte
from videoD import get_frame
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "ArchivosVideo"


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/camara')
def camara():
    return render_template('camara.html')

@app.route('/reports')
def report():
    return render_template('report.html')


@app.route('/person', methods=['POST'])
def person():
    nameP = request.form["nameP"]
    generarReporte(nameP)
    return render_template('report.html')


@app.route('/personAll', methods=['POST'])
def personAll():
    generarAllReporte()
    return render_template('report.html')


@app.route('/groupAll', methods=['POST'])
def groupAll():
    generarGroupAllReporte()
    return render_template('report.html')


@app.route('/video')
def videoD():
    return render_template('detecVideos.html')


@app.route('/videoA', methods=['POST'])
def videoPr():
    f = request.files["videoD"]
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    get_frame("ArchivosVideo\\"+filename)
    return render_template('detecVideos.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/model', methods=['POST'])
def mod():
    f = request.files["modelD"]
    filename = secure_filename(f.filename)
    f.save(os.path.join("models", filename))
    return render_template('home.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
