# crypto/diffusion.py

import numpy as np

def diffuse(data, key_stream):
    return np.bitwise_xor(data, key_stream)
