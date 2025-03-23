from bitcoinrpc.authproxy import AuthServiceProxy
import simplejson as json

def connect():
    rpc_user = "Wasd"  
    rpc_password = "8520" 
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443")
    return rpc_connection

def main():
    rpc = connect()
    with open("tx_info_final.json", "r") as f:
        legacy_tx_info = json.load(f)
    
    with open("segwit_tx_info_final.json", "r") as f:
        segwit_tx_info = json.load(f)
       
    print('debug')
    
    legacy_tx_a_to_b = rpc.getrawtransaction(legacy_tx_info["tx_a_to_b"], True)
    legacy_tx_b_to_c = rpc.getrawtransaction(legacy_tx_info["tx_b_to_c"], True)
    
    segwit_tx_a_to_b = rpc.getrawtransaction(segwit_tx_info.get("previous_transaction_id", ""), True)
    segwit_tx_b_to_c = rpc.getrawtransaction(segwit_tx_info.get("current_transaction_id", ""), True)

    
    legacy_tx_a_to_b_size = len(legacy_tx_a_to_b.get('hex', '')) // 2
    legacy_tx_b_to_c_size = len(legacy_tx_b_to_c.get('hex', '')) // 2
    
    segwit_tx_a_to_b_size = len(segwit_tx_a_to_b.get('hex', '')) // 2
    segwit_tx_b_to_c_size = len(segwit_tx_b_to_c.get('hex', '')) // 2
    
    legacy_tx_a_to_b_vsize = legacy_tx_a_to_b.get('vsize', legacy_tx_a_to_b_size)
    legacy_tx_b_to_c_vsize = legacy_tx_b_to_c.get('vsize', legacy_tx_b_to_c_size)
    
    segwit_tx_a_to_b_vsize = segwit_tx_a_to_b.get('vsize', segwit_tx_a_to_b_size)
    segwit_tx_b_to_c_vsize = segwit_tx_b_to_c.get('vsize', segwit_tx_b_to_c_size)
    
    legacy_tx_a_to_b_weight = legacy_tx_a_to_b.get('weight', 0)
    legacy_tx_b_to_c_weight = legacy_tx_b_to_c.get('weight', 0)

    segwit_tx_a_to_b_weight = segwit_tx_a_to_b.get('weight', 0)
    segwit_tx_b_to_c_weight = segwit_tx_b_to_c.get('weight', 0)
    
    print("=== TRANSACTION SIZE COMPARISON ===")
    print(f"Legacy TX (A to B): {legacy_tx_a_to_b_size} bytes, {legacy_tx_a_to_b_vsize} vbytes, {legacy_tx_a_to_b_weight} weight")
    print(f"Legacy TX (B to C): {legacy_tx_b_to_c_size} bytes, {legacy_tx_b_to_c_vsize} vbytes, {legacy_tx_b_to_c_weight} weight")
    print(f"SegWit TX (A' to B'): {segwit_tx_a_to_b_size} bytes, {segwit_tx_a_to_b_vsize} vbytes, {segwit_tx_a_to_b_weight} weight")
    print(f"SegWit TX (B' to C'): {segwit_tx_b_to_c_size} bytes, {segwit_tx_b_to_c_vsize} vbytes, {segwit_tx_b_to_c_weight} weight")
    
    legacy_total_size = legacy_tx_a_to_b_size + legacy_tx_b_to_c_size
    segwit_total_size = segwit_tx_a_to_b_size + segwit_tx_b_to_c_size
    size_diff = legacy_total_size - segwit_total_size
    size_percent = (size_diff / legacy_total_size) * 100 if legacy_total_size > 0 else 0
    
    legacy_total_vsize = legacy_tx_a_to_b_vsize + legacy_tx_b_to_c_vsize
    segwit_total_vsize = segwit_tx_a_to_b_vsize + segwit_tx_b_to_c_vsize
    vsize_diff = legacy_total_vsize - segwit_total_vsize
    vsize_percent = (vsize_diff / legacy_total_vsize) * 100 if legacy_total_vsize > 0 else 0
    
    print("\n=== SIZE DIFFERENCE ===")
    print(f"Legacy total size: {legacy_total_size} bytes, {legacy_total_vsize} vbytes")
    print(f"SegWit total size: {segwit_total_size} bytes, {segwit_total_vsize} vbytes")
    print(f"Difference: {size_diff} bytes ({size_percent:.2f}% reduction)")
    print(f"Virtual size difference: {vsize_diff} vbytes ({vsize_percent:.2f}% reduction)")

    print("\nComparison results saved to comparison_results.json")      
if __name__ == "__main__":
    main()
