# crypto/encrypt_image.py

import cv2
import numpy as np
from crypto.chaos_map import logistic_map
from crypto.diffusion import diffuse

def encrypt_image(image_path, x0, r):
    # Read image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, c = img.shape
    total = h * w * c

    # Generate chaotic key stream
    chaos = logistic_map(x0, r, total)
    chaos = (chaos * 256).astype(np.uint8)

    # Flatten image
    flat_img = img.flatten()

    # Diffusion (XOR)
    encrypted_flat = diffuse(flat_img, chaos)

    # Reshape back
    encrypted_img = encrypted_flat.reshape(h, w, c)
    return encrypted_img

