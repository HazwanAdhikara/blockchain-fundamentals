import hashlib
import json
import time

PRIVATE_KEYS = {
    "Hazwan": "key_hazwan",
    "Khapes": "key_khapes",
    "Malvin": "key_malvin",
    "Messi": "key_messi",
}

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def _message(self):
        return f"{self.sender} -> {self.receiver} : {self.amount}"

    def sign(self, private_key):
        self.signature = sha256(self._message() + private_key)

    def is_valid(self):
        if self.sender == "SYSTEM":
            return True
        
        if self.sender not in PRIVATE_KEYS:
            return False
        
        expected_signature = sha256(self._message() + PRIVATE_KEYS[self.sender])
        return expected_signature == self.signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature
        }


class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0, timestamp=None, hash=None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.timestamp = timestamp or time.time()
        self.hash = hash

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return sha256(block_string)

    def mine(self, difficulty):
        target = "0" * difficulty
        while not self.hash or not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Blok #{self.index} berhasil di-mine! Nonce: {self.nonce}, Hash: {self.hash[:20]}...")

    def to_dict(self):
        return {
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "hash": self.hash
        }


class Blockchain:
    MINING_REWARD = 5

    def __init__(self, difficulty=3):
        self.difficulty = difficulty
        self.pending_transactions = []
        self.chain = [self._genesis_block()]

    def _genesis_block(self):
        genesis = Block(0, [], "0" * 16, nonce=0)
        genesis.hash = genesis.calculate_hash()
        return genesis

    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.is_valid():
            return False, f"Transaksi tidak valid dari {transaction.sender}"
        
        self.pending_transactions.append(transaction)
        return True, f"Transaksi dari {transaction.sender} ke {transaction.receiver} sebesar {transaction.amount} berhasil ditambahkan"

    def mine_pending(self, miner_name):
        if len(self.pending_transactions) == 0:
            return False, "Tidak ada transaksi untuk di-mine"
        
        reward_tx = Transaction("SYSTEM", miner_name, self.MINING_REWARD)
        self.pending_transactions.append(reward_tx)
        
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.last_block().hash
        )
        
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        
        return True, new_block

    def replace_chain(self, new_chain_data):
        if len(new_chain_data) <= len(self.chain):
            return False, "Chain baru tidak lebih panjang"
        
        new_chain = []
        for block_data in new_chain_data:
            transactions = []
            for tx_data in block_data["transactions"]:
                tx = Transaction(
                    tx_data["sender"],
                    tx_data["receiver"],
                    tx_data["amount"],
                    tx_data["signature"]
                )
                transactions.append(tx)
            
            block = Block(
                index=block_data["index"],
                transactions=transactions,
                previous_hash=block_data["previous_hash"],
                nonce=block_data["nonce"],
                timestamp=block_data["timestamp"],
                hash=block_data["hash"]
            )
            new_chain.append(block)
        
        for i, block in enumerate(new_chain):
            if block.calculate_hash() != block.hash:
                return False, f"Hash blok #{i} tidak valid"
            
            if i > 0 and block.previous_hash != new_chain[i-1].hash:
                return False, f"Blok #{i} previous_hash tidak cocok"
            
            for tx in block.transactions:
                if not tx.is_valid():
                    return False, f"Transaksi tidak valid di blok #{i}"
        
        self.chain = new_chain
        return True, "Chain berhasil diganti dengan yang lebih panjang"

    def chain_to_dict(self):
        return [block.to_dict() for block in self.chain]
