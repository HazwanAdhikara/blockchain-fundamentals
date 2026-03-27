# Blockchain Fundamentals - Python Implementation

|Nama|NRP|
|---|---|
|Hazwan Adhikara Nasution|5027231017|
|Malvin Putra Rismahardian|5027231048|

A simple blockchain implementation with Flask REST API, digital signatures, Proof of Work mining, and multi-node synchronization.

<!-- **Group Members:** Hazwan, Khapes, Malvin (INI DIBUAT TABEL AJA NANTI + NRP) -->

---

## 📋 Features

✅ **Digital Signature** - SHA-256 based transaction signing  
✅ **Mining Reward** - 5 coins reward per mined block  
✅ **Multi-Node Network** - 3-4 nodes with automatic synchronization  
✅ **Proof of Work** - Mining with difficulty 3 (hash starts with "000")  
✅ **Flask REST API** - Complete API endpoints for blockchain operations  
✅ **Signature Validation** - Reject invalid/fake transactions

---

## 🏗️ Architecture

### Core Components

**`blockchain.py`** - Core blockchain logic

- `Transaction` class - Handle transactions with digital signatures
- `Block` class - Block structure with PoW mining
- `Blockchain` class - Chain management and validation

**`node.py`** - Flask REST API server

- Multi-node network with peer broadcasting
- Automatic chain synchronization
- Transaction mempool management

---

## 📦 Project Structure

```
blockchain-fundamentals/
├── blockchain.py       # Core blockchain implementation
├── node.py            # Flask API server
├── requirements.txt   # Python dependencies
├── img/              # Testing screenshots
└── README.md         # This file
```

---

## 🚀 How to run?

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Run Multiple Nodes

Open 3-4 separate terminals:

**Terminal 1:**

```bash
python3 node.py Hazwan 5001
```

**Terminal 2:**

```bash
python3 node.py Khapes 5002
```

**Terminal 3:**

```bash
python3 node.py Malvin 5003
```

**Terminal 4 (optional):**

```bash
python3 node.py Messi 5004
```

---

## 📡 API Endpoints

| Method | Endpoint             | Description                   |
| ------ | -------------------- | ----------------------------- |
| `GET`  | `/`                  | Node status                   |
| `POST` | `/transaksi`         | Create transaction            |
| `GET`  | `/pending`           | View pending transactions     |
| `POST` | `/mine`              | Mine new block                |
| `GET`  | `/chain`             | View entire blockchain        |
| `POST` | `/transaksi/terima`  | Receive broadcast transaction |
| `POST` | `/chain/terima-blok` | Receive block notification    |

---

## 🧪 Testing with Postman

### 1. Node Status Check

```
GET http://127.0.0.1:5001/
```

<img src="./img/node-check.png">

### 2. Create Transaction

```
POST http://127.0.0.1:5001/transaksi
Body (JSON):
{
  "receiver": "Khapes",
  "amount": 10
}
```

<img src="./img/tambah-transaksi.png">

### 3. View Pending Transactions

```
GET http://127.0.0.1:5001/pending
```

<img src="./img/transaksi-pending.png">

### 4. Mine Block

```
POST http://127.0.0.1:5001/mine
```

<img src="./img/mining.png">

### 5. View Blockchain

```
GET http://127.0.0.1:5001/chain
```

<img src="./img/get-chain.png">

---

## 🔐 Security Features

1. **Digital Signature Validation**
   - Every transaction signed with SHA-256(message + private_key)
   - Invalid signatures rejected automatically

2. **Proof of Work**
   - Mining difficulty: 3 (hash must start with "000")
   - Prevents spam and secures the network

3. **Chain Validation**
   - Verify hash integrity of each block
   - Check previous_hash linkage
   - Validate all transaction signatures

4. **Consensus Mechanism**
   - Longest chain rule
   - Automatic synchronization across nodes

---

## 📝 Assignment Requirements Checklist

✅ Digital signature implementation  
✅ Mining reward system  
✅ Minimum 3 nodes setup  
✅ Flask API + Postman testing  
✅ Source code documentation  
✅ Markdown documentation  
✅ Screenshot evidence:

- Transaction creation
- Mining process
- Miner rewards
- Digital signature validation
- Node synchronization

---

## 🛠️ Tech Stack

- **Python 3.x** - Core language
- **Flask 3.0.0** - REST API framework
- **hashlib** - SHA-256 hashing (built-in)
- **requests** - HTTP communication between nodes

---
