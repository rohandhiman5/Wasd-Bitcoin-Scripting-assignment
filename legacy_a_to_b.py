from bitcoinrpc.authproxy import AuthServiceProxy
import simplejson as json
import decimal

def connect():
    rpc_username = "Wasd"  
    rpc_password = "8520" 
    rpc_connection = AuthServiceProxy(f"http://{rpc_username}:{rpc_password}@127.0.0.1:18443")
    return rpc_connection

def main():
    rpc_client = connect()
    blockchain_details = rpc_client.getblockchaininfo()
    print(f"Connected to Bitcoin Core {blockchain_details['chain']}")

    existing_wallets = rpc_client.listwallets()
    target_wallet = "legacy_wallet"
    if target_wallet not in existing_wallets:
        print(f"Creating new wallet: {target_wallet}")
        rpc_client.createwallet(target_wallet)

    print("Generating blocks to make coins spendable")
    rpc_client.generatetoaddress(101, rpc_client.getnewaddress())

    sender_address = rpc_client.getnewaddress("", "legacy")
    receiver_address = rpc_client.getnewaddress("", "legacy")
    backup_address = rpc_client.getnewaddress("", "legacy")

    print(f"Sender Address: {sender_address}")
    print(f"Receiver Address: {receiver_address}")
    print(f"Backup Address: {backup_address}")

    print("Funding Sender Address")
    funding_tx_id = rpc_client.sendtoaddress(sender_address, 1.0)
    print(f"Funding transaction ID: {funding_tx_id}")

    rpc_client.generatetoaddress(1, rpc_client.getnewaddress())

    unspent_utxos = rpc_client.listunspent(1, 9999999, [sender_address])

    if not unspent_utxos:
        raise Exception("No unspent outputs found for the sender address")

    selected_utxo = unspent_utxos[0]

    print("Creating raw transaction from sender to receiver")
    tx_id = selected_utxo['txid']
    output_index = selected_utxo['vout']
    transfer_amount = selected_utxo['amount'] - decimal.Decimal(0.0001)

    inputs = [{"txid": tx_id, "vout": output_index}]
    outputs = {receiver_address: transfer_amount}

    raw_transaction = rpc_client.createrawtransaction(inputs, outputs)
    print(f"Raw transaction created: {raw_transaction}")

    print("Decoding raw transaction")
    decoded_transaction = rpc_client.decoderawtransaction(raw_transaction)
    print(f"ScriptPubKey for receiver address: {json.dumps(decoded_transaction['vout'][0]['scriptPubKey'], indent=2)}")

    print("Signing transaction")
    signed_transaction = rpc_client.signrawtransactionwithwallet(raw_transaction)

    if signed_transaction['complete']:
        print("Transaction signed successfully")
    else:
        raise Exception("Transaction signing failed")

    print("Broadcasting transaction")
    final_tx_id = rpc_client.sendrawtransaction(signed_transaction['hex'])
    print(f"Transaction broadcast: {final_tx_id}")

    rpc_client.generatetoaddress(1, rpc_client.getnewaddress())

    with open("tx_info.json", "w") as tx_file:
        json.dump({
            "sender_address": sender_address,
            "receiver_address": receiver_address,
            "backup_address": backup_address,
            "final_tx_id": final_tx_id
        }, tx_file)

    print("Transaction information saved to tx_info.json")

    transaction_details = rpc_client.decoderawtransaction(signed_transaction['hex'])
    print("Final Transaction Details:")
    print(json.dumps(transaction_details, indent=2))

if __name__ == "__main__":
    main()

