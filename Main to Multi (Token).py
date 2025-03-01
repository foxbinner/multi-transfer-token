from web3 import Web3

# .-.. .. - - . ..-. --- -..-
#  Constants & Configuration
# .-.. .. - - . ..-. --- -..-
AMOUNT = 0.2 # Sending amount each wallet
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
MAIN_WALLET_PRIVATE_KEY = wallet_data[3]

# Read recipient addresses
with open('recipients.txt', 'r') as file:
    RECIPIENT_ADDRESSES = [line.split(',')[1] for line in file if line.strip()]

# .-.. .. - - . ..-. --- -..-
#  Web3 Initialization
# .-.. .. - - . ..-. --- -..-
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to the chain")

# Configure gas settings
current_gas_price = web3.eth.gas_price
gas_price = current_gas_price + Web3.to_wei(GAS_ADD, 'gwei')

# Initialize main wallet
main_wallet = web3.eth.account.from_key(MAIN_WALLET_PRIVATE_KEY)

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
def send_token(recipient_address, amount_to_send, nonce):
    try:
        transaction = token_contract.functions.transfer(recipient_address, amount_to_send).build_transaction({
            "from": MAIN_WALLET_ADDRESS,
            "gas": GAS_LIMIT,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": CHAIN_ID,
        })

        # Sign and send transaction
        signed_tx = web3.eth.account.sign_transaction(transaction, MAIN_WALLET_PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # # Wait for confirmation
        # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # fee = tx_receipt['gasUsed'] * gas_price

        print(f"{recipient_address} - Amount: {AMOUNT} {TICKER} - "
              # f"Fee: {Web3.from_wei(fee, 'ether')} {TICKER} - "
              f"{EXPLORER}/tx/0x{tx_hash.hex()}")
    except Exception as e:
        print(f"Transaction failed to {recipient_address}: {str(e)}")

def check_balance(address):
    try:
        balance = token_contract.functions.balanceOf(address).call()
        return balance / (10 ** TOKEN_DECIMALS)
    except Exception as e:
        raise Exception(f"Failed to check balance: {str(e)}")

# .-.. .. - - . ..-. --- -..-
#  Execution Flow
# .-.. .. - - . ..-. --- -..-
try:
    # Initial checks
    balance = check_balance(MAIN_WALLET_ADDRESS)
    print(f"Current {TICKER} balance: {balance}\n")

    # Calculate required funds
    total_needed = AMOUNT_TO_SEND * len(RECIPIENT_ADDRESSES)

    if balance < total_needed / (10 ** TOKEN_DECIMALS):
        raise Exception(f"Insufficient balance. Need {total_needed / (10 ** TOKEN_DECIMALS)} {TICKER} to process.")

    # Transaction processing sequentially
    nonce = web3.eth.get_transaction_count(MAIN_WALLET_ADDRESS)

    for idx, recipient in enumerate(RECIPIENT_ADDRESSES):
        send_token(recipient, AMOUNT_TO_SEND, nonce + idx)

except Exception as e:
    print(f"Script error: {str(e)}")
