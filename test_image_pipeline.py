from blockchain import store_hash, verify_hash
import hashlib

# Step 1: Read image file
with open("test.jpg", "rb") as f:
    image_bytes = f.read()

# Step 2: (Optional) Encrypt image here if needed
# For now we directly hash raw image
# Later you can hash encrypted output instead

# Step 3: Generate SHA-256 hash
hash_hex = hashlib.sha256(image_bytes).hexdigest()
hash_bytes = bytes.fromhex(hash_hex)

print("Image hash:", hash_hex)

# Step 4: Store on blockchain
print("\nStoring hash on blockchain...")
store_hash("image1", hash_bytes)

# Step 5: Verify
print("\nVerifying...")
result = verify_hash("image1", hash_bytes)

print("Verification result:", result)
