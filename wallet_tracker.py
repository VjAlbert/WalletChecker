import tkinter as tk
from tkinter import ttk, messagebox
from web3 import Web3
import requests
from datetime import datetime
from etherscan import Etherscan
import time
import threading
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WalletTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("ETH Wallet Tracker")
        self.root.geometry("600x400")
        
        # Initialize Web3 and Etherscan
        infura_url = os.getenv('INFURA_URL', 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID')
        etherscan_key = os.getenv('ETHERSCAN_KEY', 'YOUR-ETHERSCAN-KEY')
        self.w3 = Web3(Web3.HTTPProvider(infura_url))
        self.etherscan = Etherscan(etherscan_key)
        
        self.current_address = None
        self.update_thread = None
        self.stop_thread = False
        
        self.setup_gui()
    
    def setup_gui(self):
        # Wallet Address Frame
        address_frame = ttk.LabelFrame(self.root, text="Indirizzo del Portafoglio", padding="10")
        address_frame.pack(fill="x", padx=10, pady=5)
        
        self.address_var = tk.StringVar()
        ttk.Entry(address_frame, textvariable=self.address_var, width=50).pack(side="left", padx=5)
        ttk.Button(address_frame, text="Traccia", command=self.track_wallet).pack(side="left", padx=5)
        
        # Balance Frame
        balance_frame = ttk.LabelFrame(self.root, text="Informazioni Portafoglio", padding="10")
        balance_frame.pack(fill="x", padx=10, pady=5)
        
        self.balance_label = ttk.Label(balance_frame, text="Saldo ETH: 0")
        self.balance_label.pack()
        
        self.price_label = ttk.Label(balance_frame, text="Prezzo ETH: $0")
        self.price_label.pack()
        
        self.value_label = ttk.Label(balance_frame, text="Valore Totale: $0")
        self.value_label.pack()
        
        # Transaction History Frame
        history_frame = ttk.LabelFrame(self.root, text="Cronologia Transazioni", padding="10")
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create Treeview for transactions
        self.tree = ttk.Treeview(history_frame, columns=("Data", "Tipo", "Quantità", "Stato"), show="headings")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Quantità", text="Quantità (ETH)")
        self.tree.heading("Stato", text="Stato")
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def update_data(self):
        while not self.stop_thread:
            if self.current_address:
                self.fetch_wallet_data(self.current_address)
            time.sleep(30)  # Update every 30 seconds
    
    def track_wallet(self):
        address = self.address_var.get()
        if not self.w3.is_address(address):
            messagebox.showerror("Errore", "Indirizzo Ethereum non valido")
            return
        
        self.current_address = address
        self.fetch_wallet_data(address)
        
        # Start update thread if not already running
        if not self.update_thread or not self.update_thread.is_alive():
            self.stop_thread = False
            self.update_thread = threading.Thread(target=self.update_data)
            self.update_thread.daemon = True
            self.update_thread.start()
    
    def fetch_wallet_data(self, address):
        try:
            # Get balance
            balance = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance, 'ether')
            
            # Get ETH price
            price_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
            eth_price = price_response.json()['ethereum']['usd']
            
            # Update labels
            self.balance_label.config(text=f"Saldo ETH: {balance_eth:.4f}")
            self.price_label.config(text=f"Prezzo ETH: ${eth_price:,.2f}")
            self.value_label.config(text=f"Valore Totale: ${(float(balance_eth) * eth_price):,.2f}")
            
            # Get transactions
            transactions = self.etherscan.get_normal_txs_by_address(address, 0, 99999999, 'desc')
            
            # Clear existing transactions
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add new transactions
            for tx in transactions[:10]:  # Show last 10 transactions
                date = datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M')
                tx_type = "Invio" if tx['from'].lower() == address.lower() else "Ricezione"
                amount = float(self.w3.from_wei(int(tx['value']), 'ether'))
                status = "Confermato" if int(tx['confirmations']) > 0 else "In attesa"
                
                self.tree.insert('', 'end', values=(date, tx_type, f"{amount:.4f}", status))
            
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile recuperare i dati del portafoglio: {str(e)}")
    
    def on_closing(self):
        self.stop_thread = True
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WalletTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()