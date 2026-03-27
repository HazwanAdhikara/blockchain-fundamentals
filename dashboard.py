import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading
import time

BG = "#1a1a2e"
BG2 = "#16213e"
ACCENT = "#0f3460"
TEXT = "#e2e8f0"
GREEN = "#22c55e"
GOLD = "#f59e0b"
RED = "#ef4444"

ALL_NODES = {
    "Hazwan": "http://127.0.0.1:5001",
    "Khapes": "http://127.0.0.1:5002",
    "Malvin": "http://127.0.0.1:5003",
    "Messi": "http://127.0.0.1:5004",
}


class BlockchainDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg=BG)
        
        self.current_node = "Hazwan"
        self.auto_refresh = True
        
        self.create_ui()
        self.start_auto_refresh()

    def create_ui(self):
        main_container = tk.Frame(self.root, bg=BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        left_panel = tk.Frame(main_container, bg=BG2, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        title = tk.Label(left_panel, text="BLOCKCHAIN\nDASHBOARD", 
                        bg=BG2, fg=GOLD, font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        tk.Label(left_panel, text="Pilih Node:", bg=BG2, fg=TEXT, font=("Arial", 10)).pack(pady=(10, 5))
        
        node_frame = tk.Frame(left_panel, bg=BG2)
        node_frame.pack(pady=5)
        
        for node in ALL_NODES.keys():
            btn = tk.Button(node_frame, text=node, bg=ACCENT, fg=TEXT, 
                          font=("Arial", 10), width=12,
                          command=lambda n=node: self.switch_node(n))
            btn.pack(pady=3)
        
        tk.Label(left_panel, text="Kirim Transaksi:", bg=BG2, fg=TEXT, font=("Arial", 10, "bold")).pack(pady=(20, 10))
        
        tk.Label(left_panel, text="Penerima:", bg=BG2, fg=TEXT, font=("Arial", 9)).pack()
        self.receiver_var = tk.StringVar(value="Khapes")
        receiver_combo = ttk.Combobox(left_panel, textvariable=self.receiver_var, 
                                     values=list(ALL_NODES.keys()), width=15)
        receiver_combo.pack(pady=5)
        
        tk.Label(left_panel, text="Jumlah:", bg=BG2, fg=TEXT, font=("Arial", 9)).pack()
        self.amount_var = tk.StringVar(value="10")
        amount_entry = tk.Entry(left_panel, textvariable=self.amount_var, width=17, 
                               bg=ACCENT, fg=TEXT, font=("Arial", 10))
        amount_entry.pack(pady=5)
        
        send_btn = tk.Button(left_panel, text="Kirim", bg=GREEN, fg="white", 
                           font=("Arial", 10, "bold"), width=15,
                           command=self.send_transaction)
        send_btn.pack(pady=10)
        
        mine_btn = tk.Button(left_panel, text="⛏ Mine Block", bg=GOLD, fg="white", 
                           font=("Arial", 10, "bold"), width=15,
                           command=self.mine_block)
        mine_btn.pack(pady=5)
        
        refresh_btn = tk.Button(left_panel, text="🔄 Refresh", bg=ACCENT, fg=TEXT, 
                              font=("Arial", 10), width=15,
                              command=self.refresh_data)
        refresh_btn.pack(pady=5)
        
        right_panel = tk.Frame(main_container, bg=BG)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(right_panel, text="Node: Hazwan | Port: 5001", 
                                     bg=ACCENT, fg=TEXT, font=("Arial", 10), anchor="w", padx=10)
        self.status_label.pack(fill=tk.X, pady=(0, 10))
        
        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        chain_tab = tk.Frame(notebook, bg=BG)
        pending_tab = tk.Frame(notebook, bg=BG)
        log_tab = tk.Frame(notebook, bg=BG)
        
        notebook.add(chain_tab, text="Chain Explorer")
        notebook.add(pending_tab, text="Pending Transactions")
        notebook.add(log_tab, text="Activity Log")
        
        self.chain_text = tk.Text(chain_tab, bg=BG2, fg=TEXT, font=("Courier", 9), 
                                 wrap=tk.WORD, state=tk.DISABLED)
        self.chain_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.pending_text = tk.Text(pending_tab, bg=BG2, fg=TEXT, font=("Courier", 9), 
                                   wrap=tk.WORD, state=tk.DISABLED)
        self.pending_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_tab, bg=BG2, fg=TEXT, font=("Courier", 9), 
                               wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def switch_node(self, node_name):
        self.current_node = node_name
        self.log(f"Switched to node: {node_name}")
        self.refresh_data()

    def log(self, message):
        def update():
            self.log_text.config(state=tk.NORMAL)
            timestamp = time.strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        self.root.after(0, update)

    def api_call(self, method, endpoint, data=None, callback=None):
        def task():
            try:
                url = ALL_NODES[self.current_node] + endpoint
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, json=data, timeout=5)
                
                result = response.json()
                if callback:
                    self.root.after(0, lambda: callback(True, result))
            except Exception as e:
                if callback:
                    self.root.after(0, lambda: callback(False, str(e)))
        
        threading.Thread(target=task, daemon=True).start()

    def refresh_data(self):
        self.log("Refreshing data...")
        self.api_call("GET", "/", callback=self.update_status)
        self.api_call("GET", "/chain", callback=self.update_chain)
        self.api_call("GET", "/pending", callback=self.update_pending)

    def update_status(self, success, data):
        if success:
            text = f"Node: {data['node']} | Port: {data['port']} | Chain: {data['panjang_chain']} blocks | Pending: {data['pending_transaksi']} tx"
            self.status_label.config(text=text)

    def update_chain(self, success, data):
        self.chain_text.config(state=tk.NORMAL)
        self.chain_text.delete(1.0, tk.END)
        
        if success:
            chain = data.get("chain", [])
            for block in chain:
                self.chain_text.insert(tk.END, f"\n{'='*80}\n", "header")
                self.chain_text.insert(tk.END, f"BLOCK #{block['index']}\n", "title")
                self.chain_text.insert(tk.END, f"{'='*80}\n", "header")
                self.chain_text.insert(tk.END, f"Hash:          {block['hash']}\n")
                self.chain_text.insert(tk.END, f"Previous Hash: {block['previous_hash']}\n")
                self.chain_text.insert(tk.END, f"Nonce:         {block['nonce']}\n")
                self.chain_text.insert(tk.END, f"Transactions:  {len(block['transactions'])}\n")
                
                for i, tx in enumerate(block['transactions'], 1):
                    self.chain_text.insert(tk.END, f"\n  TX {i}: {tx['sender']} → {tx['receiver']} : {tx['amount']}\n")
                    if tx['signature']:
                        self.chain_text.insert(tk.END, f"  Sig: {tx['signature'][:40]}...\n")
        else:
            self.chain_text.insert(tk.END, f"Error: {data}\n")
        
        self.chain_text.config(state=tk.DISABLED)

    def update_pending(self, success, data):
        self.pending_text.config(state=tk.NORMAL)
        self.pending_text.delete(1.0, tk.END)
        
        if success:
            antrian = data.get("antrian", [])
            if not antrian:
                self.pending_text.insert(tk.END, "Tidak ada transaksi pending.\n")
            else:
                for i, tx in enumerate(antrian, 1):
                    self.pending_text.insert(tk.END, f"\n{i}. {tx['sender']} → {tx['receiver']} : {tx['amount']}\n")
                    if tx['signature']:
                        self.pending_text.insert(tk.END, f"   Signature: {tx['signature'][:40]}...\n")
        else:
            self.pending_text.insert(tk.END, f"Error: {data}\n")
        
        self.pending_text.config(state=tk.DISABLED)

    def send_transaction(self):
        receiver = self.receiver_var.get()
        try:
            amount = int(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return
        
        data = {"receiver": receiver, "amount": amount}
        self.log(f"Sending {amount} to {receiver}...")
        
        def callback(success, result):
            if success:
                self.log(f"✓ Transaction sent: {result.get('pesan', 'Success')}")
                messagebox.showinfo("Success", f"Transaksi berhasil!\n{result.get('pesan', '')}")
                self.refresh_data()
            else:
                self.log(f"✗ Transaction failed: {result}")
                messagebox.showerror("Error", f"Gagal mengirim transaksi:\n{result}")
        
        self.api_call("POST", "/transaksi", data, callback)

    def mine_block(self):
        self.log("Mining block...")
        
        def callback(success, result):
            if success:
                self.log(f"✓ Block mined! Nonce: {result.get('nonce', 'N/A')}")
                messagebox.showinfo("Success", f"Block berhasil di-mine!\n{result.get('pesan', '')}")
                self.refresh_data()
            else:
                self.log(f"✗ Mining failed: {result}")
                messagebox.showerror("Error", f"Gagal mining:\n{result}")
        
        self.api_call("POST", "/mine", {}, callback)

    def start_auto_refresh(self):
        def auto_refresh_task():
            while self.auto_refresh:
                time.sleep(5)
                self.root.after(0, self.refresh_data)
        
        self.refresh_data()
        threading.Thread(target=auto_refresh_task, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainDashboard(root)
    root.mainloop()
