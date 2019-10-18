import os

from flask import Response, Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required

# from importlib import import_module
# # import camera driver
# if os.environ.get('CAMERA'):
#     Camera = import_module('camera_' + os.environ['CAMERA']).Camera
# else:
#     from camera import Camera

from camera_opencv import Camera

#DataBase
# import sqlite3
# db = sqlite3.connect('copycat.db')
# rows = db.execute('SELECT * FROM users WHERE "ID"=2')
# for row in rows:
#     print()


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        return redirect("/")
     

@app.route("/")
def index():
    """Show portfolio of stocks"""
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    """Show portfolio of stocks"""
    return render_template("quiz.html")

@app.route("/copycat")
def copycat():
    """Show portfolio of stocks"""
    return render_template("copycat.html")

#---------------------------- Camera page start -------------------------

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


#---------------------------- Camera page end -------------------------


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(debug=True)