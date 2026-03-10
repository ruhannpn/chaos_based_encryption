# chaos_based_encryptio# 🔐 Chaos + Blockchain Image Security System

A secure image protection system combining **Chaos-based XOR Encryption** with **Ethereum Blockchain integrity verification**. Images are encrypted using the Logistic Map algorithm, hashed with SHA-256, and the hash is permanently stored on a local Ethereum blockchain via a Solidity smart contract.

---

## 🚀 Features

- **Chaos Encryption** — Logistic Map XOR encryption (X0=0.487326, R=3.9999)
- **PNG Compression** — Lossless Deflate compression before encryption
- **SHA-256 Hashing** — Deterministic fingerprint of encrypted image
- **Blockchain Storage** — Hash stored on Ethereum via Solidity smart contract
- **Integrity Verification** — Detects any tampering by comparing live hash vs chain
- **Decryption** — Full image recovery using same chaos parameters
- **Web UI** — Flask-based interface for all operations

---

## 🏗️ System Architecture

```
User Upload
     ↓
PNG Compression (OpenCV Deflate Level 6)
     ↓
Chaos XOR Encryption (Logistic Map)
     ↓
SHA-256 Hash Generation
     ↓
Blockchain Storage (Ganache + Solidity)
     ↓
Verify Integrity / Decrypt Image
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Encryption | OpenCV + NumPy (Logistic Map XOR) |
| Hashing | Python hashlib (SHA-256) |
| Blockchain | Web3.py + Solidity (Ganache) |
| Smart Contract IDE | Remix IDE |
| Frontend | HTML + CSS + Jinja2 |

---

## 📁 Project Structure

```
chaos_based_encryption/
├── app.py                    # Flask app and routes
├── blockchain.py             # Web3 connection, store/verify functions
├── crypto/
│   ├── encrypt_image.py      # Logistic Map XOR encryption
│   ├── decrypt_image.py      # Logistic Map XOR decryption
│   ├── hash_utils.py         # SHA-256 generation
│   └── compress_image.py     # PNG Deflate compression
├── templates/
│   └── index.html            # Web UI
├── static/                   # Served images
├── data/
│   ├── input/                # Uploaded originals
│   └── output/               # Compressed + encrypted files
├── .env                      # Environment variables (never commit)
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/chaos-blockchain-image-security.git
cd chaos-blockchain-image-security
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install and start Ganache
```bash
npm install -g ganache
ganache
```
Or download [Ganache UI](https://trufflesuite.com/ganache/) and start it on `http://127.0.0.1:7545`

### 4. Deploy the Smart Contract
- Open [Remix IDE](https://remix.ethereum.org)
- Create and paste the `HashStorage.sol` contract
- Compiler settings: **Solidity 0.8.19**, **EVM Version: london**
- Deploy to **Custom External HTTP Provider** → `http://127.0.0.1:7545`
- Copy the deployed contract address

### 5. Configure environment variables
Create a `.env` file in the root directory:
```
INFURA_URL=http://127.0.0.1:7545
PRIVATE_KEY=your_ganache_private_key_here
CONTRACT_ADDRESS=your_deployed_contract_address_here
```

### 6. Run the application
```bash
python app.py
```
Visit `http://127.0.0.1:8080`

---

## 📜 Smart Contract (HashStorage.sol)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract HashStorage {
    mapping(string => bytes32) private hashes;

    event HashStored(string fileId, bytes32 hash);

    function storeHash(string memory fileId, bytes32 hash) public {
        hashes[fileId] = hash;
        emit HashStored(fileId, hash);
    }

    function getHash(string memory fileId) public view returns (bytes32) {
        return hashes[fileId];
    }

    function verifyHash(string memory fileId, bytes32 hash) public view returns (bool) {
        return hashes[fileId] == hash;
    }
}
```

> ⚠️ **Important:** In Remix, set EVM version to `london` before compiling to avoid the `PUSH0` invalid opcode error with Ganache.

---

## 🔒 How It Works

### Encryption
The Logistic Map equation generates a chaotic keystream:
```
Xn+1 = R × Xn × (1 - Xn)
```
Each pixel is XOR'd with a value derived from this sequence. Without the exact X0 and R values, decryption is computationally infeasible.

### Blockchain Verification
Every encrypted image has its SHA-256 hash stored on-chain via a signed Ethereum transaction. At any future point, recomputing the hash of the file and comparing it against the chain proves whether the file is authentic or tampered.

### Why Lossless PNG Compression?
JPEG is lossy — it changes pixel values slightly on each save, which would make SHA-256 non-deterministic and break verification. PNG Deflate is fully lossless, ensuring the hash is always reproducible.

---

## 🧪 Usage

| Action | Steps |
|---|---|
| Encrypt & Store | Choose image → Click "Encrypt & Store" |
| Verify Integrity | Click "Verify Integrity" |
| Decrypt Image | Click "Decrypt Image" |

---

## ⚠️ Important Notes

- **Never commit your `.env` file** — it contains your private key
- Ganache resets on restart — redeploy contract and update `CONTRACT_ADDRESS` after each restart
- This project uses a local blockchain for development — for production use Sepolia testnet or Polygon mainnet

---

## 📄 License

MIT License — free to use and modify.