# crypto/decrypt_image.py

import numpy as np
from crypto.chaos_map import logistic_map
from crypto.diffusion import diffuse

def decrypt_image(encrypted_img, x0, r):
    h, w, c = encrypted_img.shape
    total = h * w * c

    # Regenerate the SAME chaotic key stream
    chaos = logistic_map(x0, r, total)
    chaos = (chaos * 256).astype(np.uint8)

    flat_enc = encrypted_img.flatten()

    # XOR again (reverse diffusion)
    decrypted_flat = diffuse(flat_enc, chaos)

    decrypted_img = decrypted_flat.reshape(h, w, c)
    return decrypted_img
