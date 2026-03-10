from blockchain import verify_hash
import hashlib
from web3 import Web3

print("Starting test verify...")

data = b"test image data"

hash_hex = hashlib.sha256(data).hexdigest()
hash_bytes = Web3.to_bytes(hexstr=hash_hex)

print("Hash length:", len(hash_bytes))

result = verify_hash("image1", hash_bytes)

print("Verification result:", result)
