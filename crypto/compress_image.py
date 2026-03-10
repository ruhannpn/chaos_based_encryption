# crypto/compress_image.py
import cv2
import os

def compress_image(input_path, output_path, compression_level=6):
    """
    Compresses image smartly:
    - If input is JPEG → re-save as PNG with compression
    - Tracks size change honestly (can be larger for already-compressed inputs)
    """
    img = cv2.imread(input_path)

    if img is None:
        raise ValueError(f"Could not read image: {input_path}")

    # Always save as PNG for lossless pipeline
    cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, compression_level])

    original_size   = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)

    # Can be negative if PNG is larger than original JPEG
    saved_bytes = original_size - compressed_size
    ratio       = round((saved_bytes / original_size) * 100, 2)

    return {
        "original_size":   original_size,
        "compressed_size": compressed_size,
        "ratio":           ratio,
        "grew":            compressed_size > original_size
    }