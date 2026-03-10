# app.py

import os
import uuid
import cv2
from flask import Flask, request, render_template, send_file
from crypto.encrypt_image import encrypt_image

app = Flask(__name__)

UPLOAD_FOLDER = "data/input"
OUTPUT_FOLDER = "data/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Chaos key (fixed for demo)
X0 = 0.487326
R  = 3.9999


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():
    file = request.files["image"]

    # Generate unique filename (IMPORTANT)
    unique_id = str(uuid.uuid4())
    input_path = f"{UPLOAD_FOLDER}/{unique_id}.png"
    output_path = f"{OUTPUT_FOLDER}/{unique_id}_encrypted.png"

    # Save uploaded image
    file.save(input_path)

    # Encrypt
    encrypted_img = encrypt_image(input_path, X0, R)

    # Save encrypted image
    cv2.imwrite(
        output_path,
        cv2.cvtColor(encrypted_img, cv2.COLOR_RGB2BGR)
    )

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

