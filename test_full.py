from blockchain import store_hash, verify_hash
import hashlib
from web3 import Web3

print("Starting full test...")

data = b"test image data"

hash_hex = hashlib.sha256(data).hexdigest()
hash_bytes = Web3.to_bytes(hexstr=hash_hex)

print("Hash length:", len(hash_bytes))

print("\nStoring hash...")
store_hash("image1", hash_bytes)

print("\nVerifying hash...")
result = verify_hash("image1", hash_bytes)

print("Verification result:", result)
