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
        legacy_data = json.load(f)
    
    with open("segwit_tx_info_final.json", "r") as f:
        segwit_data = json.load(f)
    
    legacy_tx_ab = rpc.getrawtransaction(legacy_data["tx_a_to_b"], True)
    legacy_tx_bc = rpc.getrawtransaction(legacy_data["tx_b_to_c"], True)
    
    segwit_tx_ab = rpc.getrawtransaction(segwit_data["tx_a_to_b"], True)
    segwit_tx_bc = rpc.getrawtransaction(segwit_data["tx_b_to_c"], True)
    
    legacy_ab_size = len(legacy_tx_ab.get('hex', '')) // 2
    legacy_bc_size = len(legacy_tx_bc.get('hex', '')) // 2
    
    segwit_ab_size = len(segwit_tx_ab.get('hex', '')) // 2
    segwit_bc_size = len(segwit_tx_bc.get('hex', '')) // 2
    
    legacy_ab_vsize = legacy_tx_ab.get('vsize', legacy_ab_size)
    legacy_bc_vsize = legacy_tx_bc.get('vsize', legacy_bc_size)
    
    segwit_ab_vsize = segwit_tx_ab.get('vsize', segwit_ab_size)
    segwit_bc_vsize = segwit_tx_bc.get('vsize', segwit_bc_size)
    
    legacy_ab_weight = legacy_tx_ab.get('weight', 0)
    legacy_bc_weight = legacy_tx_bc.get('weight', 0)

    segwit_ab_weight = segwit_tx_ab.get('weight', 0)
    segwit_bc_weight = segwit_tx_bc.get('weight', 0)
    
    print("=== TRANSACTION SIZE COMPARISON ===")
    print(f"Legacy TX (A to B): {legacy_ab_size} bytes, {legacy_ab_vsize} vbytes, {legacy_ab_weight} weight")
    print(f"Legacy TX (B to C): {legacy_bc_size} bytes, {legacy_bc_vsize} vbytes, {legacy_bc_weight} weight")
    print(f"SegWit TX (A' to B'): {segwit_ab_size} bytes, {segwit_ab_vsize} vbytes, {segwit_ab_weight} weight")
    print(f"SegWit TX (B' to C'): {segwit_bc_size} bytes, {segwit_bc_vsize} vbytes, {segwit_bc_weight} weight")
    
    legacy_total_size = legacy_ab_size + legacy_bc_size
    segwit_total_size = segwit_ab_size + segwit_bc_size
    size_diff = legacy_total_size - segwit_total_size
    size_percent = (size_diff / legacy_total_size) * 100 if legacy_total_size > 0 else 0
    
    legacy_total_vsize = legacy_ab_vsize + legacy_bc_vsize
    segwit_total_vsize = segwit_ab_vsize + segwit_bc_vsize
    vsize_diff = legacy_total_vsize - segwit_total_vsize
    vsize_percent = (vsize_diff / legacy_total_vsize) * 100 if legacy_total_vsize > 0 else 0
    
    print("\n=== SIZE DIFFERENCE ===")
    print(f"Legacy total size: {legacy_total_size} bytes, {legacy_total_vsize} vbytes")
    print(f"SegWit total size: {segwit_total_size} bytes, {segwit_total_vsize} vbytes")
    print(f"Difference: {size_diff} bytes ({size_percent:.2f}% reduction)")
    print(f"Virtual size difference: {vsize_diff} vbytes ({vsize_percent:.2f}% reduction)")
    
    print("\n=== SCRIPT STRUCTURE COMPARISON ===")
    print("Legacy P2PKH:")
    print(f"  ScriptPubKey (locking script): {legacy_data['previousScriptPubKey']['asm']}")
    print(f"  ScriptSig (unlocking script): {legacy_data['scriptSig']['asm']}")
    
    print("\nSegWit P2SH-P2WPKH:")
    print(f"  ScriptPubKey (locking script): {segwit_data['previousScriptPubKey']['asm']}")
    print(f"  ScriptSig (unlocking script): {segwit_data.get('scriptSig', {}).get('asm', 'Empty (witness data used)')}")
    
    comparison = {
        "legacy": {
            "tx_a_to_b": {
                "size": legacy_ab_size,
                "vsize": legacy_ab_vsize,
                "weight": legacy_ab_weight,
                "scriptPubKey": legacy_tx_ab['vout'][0]['scriptPubKey']['asm'],
            },
            "tx_b_to_c": {
                "size": legacy_bc_size,
                "vsize": legacy_bc_vsize,
                "weight": legacy_bc_weight,
                "scriptSig": legacy_tx_bc['vin'][0]['scriptSig']['asm'],
            }
        },
        "segwit": {
            "tx_a_to_b": {
                "size": segwit_ab_size,
                "vsize": segwit_ab_vsize,
                "weight": segwit_ab_weight,
                "scriptPubKey": segwit_tx_ab['vout'][0]['scriptPubKey']['asm'],
            },
            "tx_b_to_c": {
                "size": segwit_bc_size,
                "vsize": segwit_bc_vsize,
                "weight": segwit_bc_weight,
                "scriptSig": segwit_tx_bc['vin'][0].get('scriptSig', {}).get('asm', 'Empty')
            }
        },
        "comparison": {
            "size_reduction": f"{size_percent:.2f}%",
            "vsize_reduction": f"{vsize_percent:.2f}%"
        }
    }

    with open("comparison_results.json", "w") as f:
        json.dump(comparison, f, indent=4)
    
    print("\nComparison results saved to comparison_results.json")      

if __name__ == "__main__":
    main()
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
        legacy_data = json.load(f)
    
    with open("segwit_tx_info_final.json", "r") as f:
        segwit_data = json.load(f)
    
    legacy_tx_ab = rpc.getrawtransaction(legacy_data["tx_a_to_b"], True)
    legacy_tx_bc = rpc.getrawtransaction(legacy_data["tx_b_to_c"], True)
    
    segwit_tx_ab = rpc.getrawtransaction(segwit_data["tx_a_to_b"], True)
    segwit_tx_bc = rpc.getrawtransaction(segwit_data["tx_b_to_c"], True)
    
    legacy_ab_size = len(legacy_tx_ab.get('hex', '')) // 2
    legacy_bc_size = len(legacy_tx_bc.get('hex', '')) // 2
    
    segwit_ab_size = len(segwit_tx_ab.get('hex', '')) // 2
    segwit_bc_size = len(segwit_tx_bc.get('hex', '')) // 2
    
    legacy_ab_vsize = legacy_tx_ab.get('vsize', legacy_ab_size)
    legacy_bc_vsize = legacy_tx_bc.get('vsize', legacy_bc_size)
    
    segwit_ab_vsize = segwit_tx_ab.get('vsize', segwit_ab_size)
    segwit_bc_vsize = segwit_tx_bc.get('vsize', segwit_bc_size)
    
    legacy_ab_weight = legacy_tx_ab.get('weight', 0)
    legacy_bc_weight = legacy_tx_bc.get('weight', 0)

    segwit_ab_weight = segwit_tx_ab.get('weight', 0)
    segwit_bc_weight = segwit_tx_bc.get('weight', 0)
    
    print("=== TRANSACTION SIZE COMPARISON ===")
    print(f"Legacy TX (A to B): {legacy_ab_size} bytes, {legacy_ab_vsize} vbytes, {legacy_ab_weight} weight")
    print(f"Legacy TX (B to C): {legacy_bc_size} bytes, {legacy_bc_vsize} vbytes, {legacy_bc_weight} weight")
    print(f"SegWit TX (A' to B'): {segwit_ab_size} bytes, {segwit_ab_vsize} vbytes, {segwit_ab_weight} weight")
    print(f"SegWit TX (B' to C'): {segwit_bc_size} bytes, {segwit_bc_vsize} vbytes, {segwit_bc_weight} weight")
    
    legacy_total_size = legacy_ab_size + legacy_bc_size
    segwit_total_size = segwit_ab_size + segwit_bc_size
    size_diff = legacy_total_size - segwit_total_size
    size_percent = (size_diff / legacy_total_size) * 100 if legacy_total_size > 0 else 0
    
    legacy_total_vsize = legacy_ab_vsize + legacy_bc_vsize
    segwit_total_vsize = segwit_ab_vsize + segwit_bc_vsize
    vsize_diff = legacy_total_vsize - segwit_total_vsize
    vsize_percent = (vsize_diff / legacy_total_vsize) * 100 if legacy_total_vsize > 0 else 0
    
    print("\n=== SIZE DIFFERENCE ===")
    print(f"Legacy total size: {legacy_total_size} bytes, {legacy_total_vsize} vbytes")
    print(f"SegWit total size: {segwit_total_size} bytes, {segwit_total_vsize} vbytes")
    print(f"Difference: {size_diff} bytes ({size_percent:.2f}% reduction)")
    print(f"Virtual size difference: {vsize_diff} vbytes ({vsize_percent:.2f}% reduction)")
    
    print("\n=== SCRIPT STRUCTURE COMPARISON ===")
    print("Legacy P2PKH:")
    print(f"  ScriptPubKey (locking script): {legacy_data['previousScriptPubKey']['asm']}")
    print(f"  ScriptSig (unlocking script): {legacy_data['scriptSig']['asm']}")
    
    print("\nSegWit P2SH-P2WPKH:")
    print(f"  ScriptPubKey (locking script): {segwit_data['previousScriptPubKey']['asm']}")
    print(f"  ScriptSig (unlocking script): {segwit_data.get('scriptSig', {}).get('asm', 'Empty (witness data used)')}")
    
    comparison = {
        "legacy": {
            "tx_a_to_b": {
                "size": legacy_ab_size,
                "vsize": legacy_ab_vsize,
                "weight": legacy_ab_weight,
                "scriptPubKey": legacy_tx_ab['vout'][0]['scriptPubKey']['asm'],
            },
            "tx_b_to_c": {
                "size": legacy_bc_size,
                "vsize": legacy_bc_vsize,
                "weight": legacy_bc_weight,
                "scriptSig": legacy_tx_bc['vin'][0]['scriptSig']['asm'],
            }
        },
        "segwit": {
            "tx_a_to_b": {
                "size": segwit_ab_size,
                "vsize": segwit_ab_vsize,
                "weight": segwit_ab_weight,
                "scriptPubKey": segwit_tx_ab['vout'][0]['scriptPubKey']['asm'],
            },
            "tx_b_to_c": {
                "size": segwit_bc_size,
                "vsize": segwit_bc_vsize,
                "weight": segwit_bc_weight,
                "scriptSig": segwit_tx_bc['vin'][0].get('scriptSig', {}).get('asm', 'Empty')
            }
        },
        "comparison": {
            "size_reduction": f"{size_percent:.2f}%",
            "vsize_reduction": f"{vsize_percent:.2f}%"
        }
    }

    with open("comparison_results.json", "w") as f:
        json.dump(comparison, f, indent=4)
    
    print("\nComparison results saved to comparison_results.json")      

if __name__ == "__main__":
    main()

