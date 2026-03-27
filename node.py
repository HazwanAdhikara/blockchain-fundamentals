import sys
from flask import Flask, request, jsonify
import requests
from blockchain import Blockchain, Transaction, PRIVATE_KEYS

if len(sys.argv) != 3:
    print("Usage: python node.py <nama> <port>")
    print("Contoh: python node.py Messi 5004")
    sys.exit(1)

NODE_NAME = sys.argv[1]
NODE_PORT = int(sys.argv[2])

ALL_NODES = {
    "Hazwan": "http://127.0.0.1:5001",
    "Khapes": "http://127.0.0.1:5002",
    "Malvin": "http://127.0.0.1:5003",
    "Messi": "http://127.0.0.1:5004",
}

PEERS = {name: url for name, url in ALL_NODES.items() if name != NODE_NAME}

app = Flask(__name__)
bc = Blockchain()


def broadcast(endpoint, payload):
    for name, url in PEERS.items():
        try:
            requests.post(url + endpoint, json=payload, timeout=3)
            print(f"✓ Broadcast ke {name}: {endpoint}")
        except Exception as e:
            print(f"✗ Gagal broadcast ke {name}: {str(e)}")


def sinkronisasi():
    replaced = False
    for name, url in PEERS.items():
        try:
            response = requests.get(url + "/chain", timeout=3)
            data = response.json()
            ok, msg = bc.replace_chain(data["chain"])
            if ok:
                print(f"✓ Chain diganti dari {name}: {msg}")
                replaced = True
        except Exception as e:
            print(f"✗ Gagal sinkronisasi dari {name}: {str(e)}")
    return replaced


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "node": NODE_NAME,
        "port": NODE_PORT,
        "panjang_chain": len(bc.chain),
        "pending_transaksi": len(bc.pending_transactions)
    })


@app.route("/transaksi", methods=["POST"])
def create_transaction():
    data = request.get_json()
    receiver = data.get("receiver")
    amount = data.get("amount")
    
    if not receiver or amount is None:
        return jsonify({"error": "receiver dan amount wajib diisi"}), 400
    
    tx = Transaction(NODE_NAME, receiver, amount)
    tx.sign(PRIVATE_KEYS[NODE_NAME])
    
    ok, msg = bc.add_transaction(tx)
    if not ok:
        return jsonify({"error": msg}), 400
    
    broadcast("/transaksi/terima", tx.to_dict())
    
    return jsonify({
        "pesan": msg,
        "signature": tx.signature[:20] + "...",
        "jumlah_antrian": len(bc.pending_transactions)
    }), 200


@app.route("/transaksi/terima", methods=["POST"])
def receive_transaction():
    data = request.get_json()
    tx = Transaction(
        data["sender"],
        data["receiver"],
        data["amount"],
        data["signature"]
    )
    
    ok, msg = bc.add_transaction(tx)
    if not ok:
        print(f"⚠ Transaksi ditolak: {msg}")
    else:
        print(f"✓ Transaksi diterima: {msg}")
    
    return jsonify({"pesan": msg, "ok": ok}), 200


@app.route("/mine", methods=["POST"])
def mine_block():
    ok, result = bc.mine_pending(NODE_NAME)
    if not ok:
        return jsonify({"error": result}), 400
    
    broadcast("/chain/terima-blok", result.to_dict())
    
    return jsonify({
        "pesan": f"Blok #{result.index} berhasil di-mine!",
        "nonce": result.nonce,
        "hash": result.hash[:20] + "...",
        "jumlah_transaksi": len(result.transactions),
        "reward": bc.MINING_REWARD
    }), 200


@app.route("/chain/terima-blok", methods=["POST"])
def receive_block():
    replaced = sinkronisasi()
    pesan = "Chain disinkronisasi" if replaced else "Chain sudah terbaru"
    return jsonify({"pesan": pesan}), 200


@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify({
        "node": NODE_NAME,
        "panjang": len(bc.chain),
        "chain": bc.chain_to_dict()
    }), 200


@app.route("/pending", methods=["GET"])
def get_pending():
    return jsonify({
        "node": NODE_NAME,
        "jumlah": len(bc.pending_transactions),
        "antrian": [tx.to_dict() for tx in bc.pending_transactions]
    }), 200


if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"🚀 Node {NODE_NAME} berjalan di port {NODE_PORT}")
    print(f"{'='*50}\n")
    app.run(host="127.0.0.1", port=NODE_PORT, debug=False)
