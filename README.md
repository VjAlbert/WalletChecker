Python ETH Wallet Tracker Documentation

The provided Python script implements a graphical user interface (GUI) application to track Ethereum (ETH) wallet balances and transactions. The application uses various Python libraries for its functionality:

Key Components:

1. Environment Variables (.env file):

INFURA_URL: URL used for connecting to the Ethereum network via Infura.

ETHERSCAN_KEY: API key for accessing Etherscan services.

2. Dependencies (requirements.txt):

web3: For blockchain interactions (Ethereum).

etherscan-python: Interact with Etherscan API.

requests: HTTP requests for getting ETH price.

Application Structure:

Class: WalletTracker

Manages application logic and user interactions.

Methods:

__init__(self, root): Initializes the GUI window and Ethereum connection using environment variables.

setup_gui(self): Constructs the user interface elements:

Wallet address input field.

Display of wallet balance, ETH price, and total wallet value.

Transaction history displayed via a scrollable tree view.

track_wallet(self): Validates the wallet address and initiates data fetching and tracking.

fetch_wallet_data(self, address): Retrieves and displays wallet balance, current ETH price (from CoinGecko API), and the latest transactions (via Etherscan API).

update_data(self): Periodically (every 30 seconds) refreshes wallet data to provide real-time updates.

on_closing(self): Gracefully stops background processes and closes the application.

Functionality:

Wallet Balance & ETH Price: Shows the wallet’s ETH balance and its equivalent in USD based on current market prices.

Transaction History: Lists the most recent ten transactions, specifying date, transaction type (send/receive), amount, and transaction status (confirmed/pending).

Real-Time Updates: Continuously refreshes wallet data to ensure current information.

Running the Application:

Ensure .env file and requirements.txt are correctly set up.

Run the application using:

python wallet_tracker.py

GUI Overview:

User-friendly interface built with Tkinter for straightforward user interaction and clear presentation of wallet information.

