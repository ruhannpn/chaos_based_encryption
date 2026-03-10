# main.py

import cv2
from crypto.encrypt_image import encrypt_image

x0 = 0.487326
r  = 3.9999

encrypted = encrypt_image(
    "data/input/image.png",
    x0,
    r
)

cv2.imwrite(
    "data/output/encrypted.png",
    cv2.cvtColor(encrypted, cv2.COLOR_RGB2BGR)
)

print("Encryption complete.")
