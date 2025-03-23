from bitcoinrpc.authproxy import AuthServiceProxy
import simplejson as json
import decimal

def connect_to_node():
    username = "Wasd"  # Replace with your Bitcoin Core RPC username
    password = "8520"  # Replace with your Bitcoin Core RPC password
    wallet_identifier = "segwit_wallet"  # Wallet name
    rpc_client = AuthServiceProxy(f"http://{username}:{password}@127.0.0.1:18443/wallet/{wallet_identifier}")
    return rpc_client

def main():
    rpc = connect_to_node()
    wallet_identifier = "segwit_wallet"

    # Ensure wallet is loaded
    if wallet_identifier not in rpc.listwallets():
        print(f"Loading wallet: {wallet_identifier}")
        rpc.loadwallet(wallet_identifier)
    
    with open("segwit_tx_info.json", "r") as file:
        transaction_data = json.load(file)

    intermediary_address = transaction_data["address_b_prime"]
    receiver_address = transaction_data["address_c_prime"]
    previous_transaction_id = transaction_data["tx_a_to_b"]

    print(f"Intermediary Address B': {intermediary_address}")
    print(f"Receiver Address C': {receiver_address}")
    print(f"Previous Transaction (A' to B'): {previous_transaction_id}")

    available_utxos = rpc.listunspent(1, 9999999, [intermediary_address])

    if not available_utxos:
        raise Exception("No unspent outputs found for Intermediary Address B'")

    selected_utxo = None
    for output in available_utxos:
        if output['txid'] == previous_transaction_id:
            selected_utxo = output
            break

    if not selected_utxo:
        raise Exception(f"Could not find UTXO from transaction {previous_transaction_id}")

    print(f"Selected UTXO: {selected_utxo}")

    print("Creating raw transaction from B' to C'")
    input_txid = selected_utxo['txid']
    input_vout_index = selected_utxo['vout']
    transfer_amount = selected_utxo['amount'] - decimal.Decimal(0.0001)  # Deduct small fee

    transaction_inputs = [{"txid": input_txid, "vout": input_vout_index}]
    transaction_outputs = {receiver_address: transfer_amount}

    raw_transaction = rpc.createrawtransaction(transaction_inputs, transaction_outputs)
    print(f"Raw Transaction Created: {raw_transaction}")

    print("Decoding raw transaction...")
    decoded_raw_transaction = rpc.decoderawtransaction(raw_transaction)
    print(f"Decoded Raw Transaction: {json.dumps(decoded_raw_transaction, indent=2)}")

    print("Signing the transaction...")
    signed_transaction = rpc.signrawtransactionwithwallet(raw_transaction)

    if not signed_transaction['complete']:
        raise Exception("Transaction signing failed")

    decoded_signed_transaction = rpc.decoderawtransaction(signed_transaction['hex'])
    print("Signed Transaction Details:")
    print(json.dumps(decoded_signed_transaction, indent=2))

    print("Broadcasting the transaction...")
    broadcasted_transaction_id = rpc.sendrawtransaction(signed_transaction['hex'])
    print(f"Transaction from B' to C' broadcasted: {broadcasted_transaction_id}")

    # Generate a block to confirm the transaction
    rpc.generatetoaddress(1, rpc.getnewaddress())
    print("Transaction confirmed!")

    # Save final transaction details
    with open("segwit_tx_info_final.json", "w") as file:
        json.dump({
            "sender_address_a_prime": transaction_data["address_a_prime"],
            "intermediary_address_b_prime": intermediary_address,
            "receiver_address_c_prime": receiver_address,
            "previous_transaction_id": previous_transaction_id,
            "current_transaction_id": broadcasted_transaction_id
        }, file)

    print("Final transaction information saved to segwit_tx_info_final.json")

    # Unload the wallet after completion
    rpc.unloadwallet(wallet_identifier)

if __name__ == "__main__":
    main()

