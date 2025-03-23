# Bitcoin Scripting Assignment

This repository contains the implementation for **Assignment 3** of the course **CS - 216 : Introduciton to Blockchain**.

## Team Name: 
WASD

## Team Members
- **Rohan Dhiman**  
  **Roll No.:** 230001069  
- **Mani Kaustubh Mathur**  
  **Roll No.:** 230001050  
- **Siddharth Singh**  
  **Roll No.:** 230002068  

## Objective
This assignment explores the process of creating and validating Bitcoin transactions using both **Legacy (P2PKH)** and **SegWit (P2SH-P2WPKH)** address formats. The implementation includes code to interact with **bitcoind**, create transactions, and analyze the scripts involved.

## Requirements
- **Bitcoin Core (bitcoind)**
- **Python 3.x**

### Required Python Packages:
```bash
pip install python-bitcoinrpc simplejson
```

## Setup Instructions
1. Install **Bitcoin Core** and configure it to run in **regtest mode**.
2. Update your `bitcoin.conf` file with the following settings:

   ```ini
   regtest=1
   server=1
   rpcuser=Wasd
   rpcpassword=8520
   paytxfee=0.0001
   fallbackfee=0.0002
   mintxfee=0.00001
   txconfirmtarget=1
   ```

3. Start **Bitcoin Core** in regtest mode:

   ```bash
   bitcoind -regtest
   ```

## Project Structure
- `legacy_a_to_b.py` - Script to create and broadcast a transaction from **Legacy address A to B**
- `legacy_b_to_c.py` - Script to create and broadcast a transaction from **Legacy address B to C**
- `segwit_a_to_b.py` - Script to create and broadcast a transaction from **SegWit address A' to B'**
- `segwit_b_to_c.py` - Script to create and broadcast a transaction from **SegWit address B' to C'**
- `report.pdf` - Detailed analysis of the transactions and scripts

## Running the Code

### Part 1: Legacy Address Transactions
To create a transaction from address A to B:
```bash
python legacy_a_to_b.py
```

To create a transaction from address B to C:
```bash
python legacy_b_to_c.py
```

### Part 2: SegWit Address Transactions
To create a transaction from address A' to B':
```bash
python segwit_a_to_b.py
```

To create a transaction from address B' to C':
```bash
python segwit_b_to_c.py
```

## Analysis
The repository includes a detailed analysis comparing:
- Transaction sizes between **P2PKH** and **P2SH-P2WPKH**
- Script structures and their differences
- Benefits of **SegWit transactions**

For detailed analysis and screenshots of the decoded scripts, please refer to the **report.pdf** file.

