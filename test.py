# test.py - run this standalone
from blockchain import contract, w3

try:
    result = contract.functions.getHash("image1").call()
    print("✅ getHash works:", result.hex())
except Exception as e:
    print("❌ getHash failed:", e)