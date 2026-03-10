import hashlib
from blockchain import verify_hash

data = b"test_image_data"

hash_bytes = hashlib.sha256(data).digest()

result = verify_hash("image1", hash_bytes)

print("Verification result:", result)
