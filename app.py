from flask import Flask, render_template, request, send_file
import os
import cv2
import json
import shutil

from crypto.encrypt_image import encrypt_image
from crypto.decrypt_image import decrypt_image
from crypto.hash_utils import generate_sha256
from crypto.compress_image import compress_image
from blockchain import store_hash, verify_hash, contract, w3

app = Flask(__name__)

UPLOAD_FOLDER = "data/input"
ENC_FOLDER    = "data/output"
STATIC_FOLDER = "static"
ID_FILE       = "data/last_file_id.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENC_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

x0 = 0.487326
r  = 3.9999


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("image")
    if not file:
        return "No file uploaded"

    original_path   = os.path.join(UPLOAD_FOLDER, file.filename)
    compressed_path = os.path.join(ENC_FOLDER, "compressed.png")
    encrypted_path  = os.path.join(ENC_FOLDER, "encrypted.png")

    file.save(original_path)

    # Copy original to static for display
    shutil.copy(original_path, "static/original.png")

    # ── STEP 1: Compress original image ──────────────
    compression_info = compress_image(original_path, compressed_path)

    original_kb   = round(compression_info["original_size"] / 1024, 2)
    compressed_kb = round(compression_info["compressed_size"] / 1024, 2)
    ratio         = compression_info["ratio"]

    # ── STEP 2: Encrypt compressed image ─────────────
    encrypted_img = encrypt_image(compressed_path, x0, r)
    cv2.imwrite(encrypted_path, cv2.cvtColor(encrypted_img, cv2.COLOR_RGB2BGR))

    # Copy encrypted to static for display
    shutil.copy(encrypted_path, "static/encrypted.png")

    # ── STEP 3: Hash encrypted file ──────────────────
    hash_hex   = generate_sha256(encrypted_path)
    hash_bytes = bytes.fromhex(hash_hex)

    # Save file_id for verify/decrypt routes
    file_id = file.filename
    with open(ID_FILE, "w") as f:
        json.dump({"file_id": file_id}, f)

    # ── STEP 4: Store on blockchain + get receipt ─────
    tx_hash    = store_hash(file_id, hash_bytes)
    receipt    = w3.eth.get_transaction_receipt(tx_hash)
    chain_hash = contract.functions.getHash(file_id).call().hex()

    return render_template(
        "index.html",
        message="✅ Upload Successful",
        tx_hash=tx_hash,
        block_number=receipt.blockNumber,
        gas_used=receipt.gasUsed,
        stored_hash=hash_hex,
        chain_hash=chain_hash,
        original_image="original.png",
        encrypted_image="encrypted.png",
        original_kb=original_kb,
        compressed_kb=compressed_kb,
        compression_ratio=ratio
    )


@app.route("/verify", methods=["POST"])
def verify():
    encrypted_path = os.path.join(ENC_FOLDER, "encrypted.png")

    if not os.path.exists(encrypted_path):
        return render_template("index.html", verification="No encrypted file found")

    if not os.path.exists(ID_FILE):
        return render_template("index.html", verification="No upload record found. Please upload first.")

    with open(ID_FILE) as f:
        file_id = json.load(f)["file_id"]

    hash_hex   = generate_sha256(encrypted_path)
    hash_bytes = bytes.fromhex(hash_hex)

    result = verify_hash(file_id, hash_bytes)

    return render_template(
        "index.html",
        verify_result=result,
        verify_hash=hash_hex
    )


@app.route("/decrypt", methods=["POST"])
def decrypt():
    encrypted_path = os.path.join(ENC_FOLDER, "encrypted.png")
    decrypted_path = "static/decrypted.png"

    if not os.path.exists(encrypted_path):
        return render_template("index.html", verification="No encrypted file available")

    img = cv2.imread(encrypted_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    decrypted = decrypt_image(img, x0, r)
    cv2.imwrite(decrypted_path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))

    return render_template(
        "index.html",
        decrypted_image="decrypted.png"
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)