from bitcoinrpc.authproxy import AuthServiceProxy
import simplejson as json
import decimal

def connect():
 
    rpc_user = "Wasd"
    rpc_password = "8520"
    rpc_port = "18443"
    
    wallet_name = "segwit_wallet"
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")
    
    return rpc_connection

def main():
    rpc = connect()

    try:
        blockchain_info = rpc.getblockchaininfo()
        print(f"Connected to Bitcoin Core (Network: {blockchain_info['chain']})")
    except Exception as e:
        print(f"Failed to connect to Bitcoin Core: {e}")
        return

   
    wallet_name = "segwit_wallet"
    existing_wallets = rpc.listwallets()
    
    if wallet_name not in existing_wallets:
        print(f"Creating new wallet: {wallet_name}")
        try:
            rpc.createwallet(wallet_name)
        except Exception as e:
            print(f"Error creating wallet: {e}")
            return
    else:
        print(f"Using existing wallet: {wallet_name}")

   
    print("Generating 101 blocks to make coins spendable...")
    try:
        address_for_mining = rpc.getnewaddress()
        rpc.generatetoaddress(101, address_for_mining)
        print(f"Blocks generated. Mining address: {address_for_mining}")
    except Exception as e:
        print(f"Error generating blocks: {e}")
        return

   
    address_a_prime = rpc.getnewaddress("", "p2sh-segwit")
    address_b_prime = rpc.getnewaddress("", "p2sh-segwit")
    address_c_prime = rpc.getnewaddress("", "p2sh-segwit")

    print(f"Address A': {address_a_prime}")
    print(f"Address B': {address_b_prime}")
    print(f"Address C': {address_c_prime}")

  
    print(f"Funding Address A' with 1 BTC...")
    try:
        txid_funding = rpc.sendtoaddress(address_a_prime, 1.0)
        print(f"Funding transaction ID: {txid_funding}")
        rpc.generatetoaddress(1, address_for_mining)  # Confirm the transaction
    except Exception as e:
        print(f"Error funding Address A': {e}")
        return

   
    print("Fetching UTXOs for Address A'...")
    unspent_outputs = rpc.listunspent(1, 9999999, [address_a_prime])
    
    if not unspent_outputs:
        print("No unspent outputs found. Exiting...")
        return

    utxo = unspent_outputs[0]
    txid = utxo['txid']
    vout = utxo['vout']
    amount = utxo['amount'] - decimal.Decimal(0.0001)  # Subtracting minimal fee

    
    print("Creating raw transaction from A' to B'...")
    raw_inputs = [{"txid": txid, "vout": vout}]
    raw_outputs = {address_b_prime: amount}

    try:
        raw_tx = rpc.createrawtransaction(raw_inputs, raw_outputs)
        print(f"Raw transaction created: {raw_tx}")

        
        decoded_tx = rpc.decoderawtransaction(raw_tx)
        print("Decoded transaction:")
        print(json.dumps(decoded_tx, indent=2))
    except Exception as e:
        print(f"Error creating or decoding raw transaction: {e}")
        return

    print("Signing the transaction...")
    signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

    if not signed_tx['complete']:
        print("Transaction signing failed. Exiting...")
        return

    
    try:
        tx_a_to_b = rpc.sendrawtransaction(signed_tx['hex'])
        print(f"Transaction broadcast successfully. TXID: {tx_a_to_b}")
        rpc.generatetoaddress(1, address_for_mining)  # Confirm the transaction
    except Exception as e:
        print(f"Error broadcasting transaction: {e}")
        return

    
    print("Saving transaction information to 'segwit_tx_info.json'...")
    with open("segwit_tx_info.json", "w") as f:
        json.dump({
            "address_a_prime": address_a_prime,
            "address_b_prime": address_b_prime,
            "address_c_prime": address_c_prime,
            "tx_a_to_b": tx_a_to_b
        }, f)

    
    print("Final Transaction Details:")
    print(json.dumps(rpc.decoderawtransaction(signed_tx['hex']), indent=2))

if __name__ == "__main__":
    main()
