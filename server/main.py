import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import image_processing

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_boolean(value):
    if value == "False":
        return False
    elif value == "True":
        return True


@app.route("/api/v1/version")
def version():
    return jsonify(status="success", message="1.0"), 200


@app.route("/api/v1/image_processing", methods=["POST"])
def image_processing_func():
    # check if the post request has the file part
    if "file" not in request.files:
        return jsonify(status="error", message="No file part"), 401

    print(request.form)
    flags = request.form["flags"].split(", ")
    state = {
        "color_in_hand": request.form["color_in_hand"],
        "mode": request.form["mode"],
        "flags": {
            "red": get_boolean(flags[0]),
            "blue": get_boolean(flags[1]),
            "green": get_boolean(flags[2]),
        },
    }
    print(state)
    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        print("File is saved!")
        x, y, color_in_hand = image_processing.main(
            imagename=filename,
            imagepath=filepath,
            mode=state["mode"],
            flags=state["flags"],
            color_in_hand=state["color_in_hand"],
        )
        print("Return")
        return (
            jsonify(
                status="success",
                x=x,
                y=y,
                color_in_hand=color_in_hand,
                message="Processed Image",
            ),
            200,
        )

    return jsonify(status="error", message="Something is wrong"), 401


"""
@app.route("/api/v1/upload_image", methods=["POST"])
def upload_image():
    # check if the post request has the file part
    if "file" not in request.files:
        return jsonify(status="error", message="No file part"), 401

    file = request.files["file"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify(status="success", message="Uploaded file"), 200

    return jsonify(status="error", message="Something is wrong"), 401


@app.route("/api/v1/image_processing/<filename>", methods=["POST"])
def image_processing(filename):
    pass
"""


@app.route("/api/v1/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

