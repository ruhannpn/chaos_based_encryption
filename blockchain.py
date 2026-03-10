from web3 import Web3
import os
from dotenv import load_dotenv

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# -----------------------------
# CONNECT TO GANACHE
# -----------------------------
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise Exception("❌ Web3 not connected. Check INFURA_URL")

print("✅ Connected to blockchain")
print("Chain ID:", w3.eth.chain_id)

# -----------------------------
# LOAD ACCOUNT
# -----------------------------
account = w3.eth.account.from_key(PRIVATE_KEY)
w3.eth.default_account = account.address

print("Using wallet:", account.address)

# -----------------------------
# CONTRACT ADDRESS
# -----------------------------
contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

print("Using contract address:", contract_address)

# -----------------------------
# CONTRACT ABI
# -----------------------------
abi = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "string", "name": "fileId", "type": "string"},
            {"indexed": False, "internalType": "bytes32", "name": "hash", "type": "bytes32"}
        ],
        "name": "HashStored",
        "type": "event"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "fileId", "type": "string"},
            {"internalType": "bytes32", "name": "hash", "type": "bytes32"}
        ],
        "name": "storeHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "fileId", "type": "string"}
        ],
        "name": "getHash",
        "outputs": [
            {"internalType": "bytes32", "name": "", "type": "bytes32"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "string", "name": "fileId", "type": "string"},
            {"internalType": "bytes32", "name": "hash", "type": "bytes32"}
        ],
        "name": "verifyHash",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# -----------------------------
# CREATE CONTRACT INSTANCE
# -----------------------------
contract = w3.eth.contract(address=contract_address, abi=abi)

print("Contract loaded")
print("Block number:", w3.eth.block_number)



# -----------------------------
# STORE HASH
# -----------------------------
def store_hash(file_id, hash_bytes):

    # Ensure bytes32 format
    if isinstance(hash_bytes, bytes):
        hash_bytes32 = hash_bytes[:32]
    else:
        hash_bytes32 = bytes.fromhex(hash_bytes)[:32]

    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.storeHash(file_id, hash_bytes32).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("2", "gwei"),
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("✅ Transaction mined:", tx_hash.hex())

    return tx_hash.hex()


# -----------------------------
# VERIFY HASH
# -----------------------------
def verify_hash(file_id, hash_bytes):

    try:

        stored = contract.functions.getHash(file_id).call()

        # convert incoming hash properly
        if isinstance(hash_bytes, bytes):
            incoming = hash_bytes[:32]
        else:
            incoming = bytes.fromhex(hash_bytes)[:32]

        print("Stored:", stored.hex())
        print("Incoming:", incoming.hex())

        return stored == incoming

    except Exception as e:

        print("❌ Error verifying hash:", e)
        return None