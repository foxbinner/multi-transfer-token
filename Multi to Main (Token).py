from web3 import Web3

# .-.. .. - - . ..-. --- -..-
#  Constants & Configuration
# .-.. .. - - . ..-. --- -..-
AMOUNT = 0 # Put 0 to send all
RPC_URL = 'https://ethereum-sepolia-rpc.publicnode.com'
CHAIN_ID = 11155111
TOKEN_CONTRACT = '0xadbf21cCdFfe308a8d83AC933EF5D3c98830397F'
TICKER = 'USDC'
EXPLORER = 'https://sepolia.etherscan.io'
GAS_LIMIT = 60000  # Fixed gas limit
GAS_ADD = 1  # Put 0 for minimum gas fee

# .-.. .. - - . ..-. --- -..-
#   File Configuration
# .-.. .. - - . ..-. --- -..-
# Read main wallet credentials
with open('mainwallet.txt', 'r') as file:
    line = file.readline().strip()
wallet_data = line.split(',')
MAIN_WALLET_ADDRESS = wallet_data[1]

# Load sender credentials
with open('recipients.txt', 'r') as file:
    SENDER_ADDRESSES_AND_KEYS = [line.strip().split(',') for line in file if line.strip()]

# .-.. .. - - . ..-. --- -..-
#  Web3 Initialization
# .-.. .. - - . ..-. --- -..-
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to the chain")

# Configure gas settings
current_gas_price = web3.eth.gas_price
gas_price = current_gas_price + Web3.to_wei(GAS_ADD, 'gwei')

# .-.. .. - - . ..-. --- -..-
#  ERC20 Token ABI (Minimum Required Functions)
# .-.. .. - - . ..-. --- -..-
TOKEN_ABI = [
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# .-.. .. - - . ..-. --- -..-
#  Contract & Decimals Setup
# .-.. .. - - . ..-. --- -..-
token_contract = web3.eth.contract(address=TOKEN_CONTRACT, abi=TOKEN_ABI)
TOKEN_DECIMALS = token_contract.functions.decimals().call()
AMOUNT_TO_SEND = int(AMOUNT * (10 ** TOKEN_DECIMALS))

# .-.. .. - - . ..-. --- -..-
#  Core Functions
# .-.. .. - - . ..-. --- -..-
if AMOUNT == 0:
    print(f"Sending All {TICKER}:\n")
else:
    print(f"Sending {AMOUNT} {TICKER}:\n")

def send_token(sender_address, sender_private_key, nonce):
    try:
        token_balance = token_contract.functions.balanceOf(sender_address).call()
        native_balance = web3.eth.get_balance(sender_address)
        gas_fee = GAS_LIMIT * gas_price

        if token_balance <= 0 or native_balance <= gas_fee:
            print(f"Skipping {sender_address} - Balance: {token_balance / (10 ** TOKEN_DECIMALS):.4f} {TICKER} - Gas: {native_balance / 1e18:.8f}")
            return

        if AMOUNT == 0:
            amount_to_send = token_balance
        else:
            amount_to_send = AMOUNT_TO_SEND

        transaction = token_contract.functions.transfer(sender_address, amount_to_send).build_transaction({
            "from": sender_address,
            "gas": GAS_LIMIT,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": CHAIN_ID,
        })

        # Sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, sender_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # # Wait for confirmation
        # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # fee = tx_receipt['gasUsed'] * gas_price

        print(f"{sender_address} - Amount: {amount_to_send / (10 ** TOKEN_DECIMALS)} {TICKER} - "
              # f"Fee: {Web3.from_wei(fee, 'ether')} {TICKER} - "
              f"{EXPLORER}/tx/0x{tx_hash.hex()}")
    except Exception as e:
        print(f"Transaction failed from {sender_address}: {str(e)}")

# .-.. .. - - . ..-. --- -..-
#  Execution Flow
# .-.. .. - - . ..-. --- -..-
try:
    for sender_data in SENDER_ADDRESSES_AND_KEYS:
        sender_address = sender_data[1]
        sender_private_key = sender_data[3]
        nonce = web3.eth.get_transaction_count(sender_address)
        send_token(sender_address, sender_private_key, nonce)

except Exception as e:
    print(f"Script error: {str(e)}")