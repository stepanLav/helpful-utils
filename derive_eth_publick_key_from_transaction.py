import web3
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS, serializable_unsigned_transaction_from_dict

'''
For derive publick key from ETH transaction:
1. Set blockchain node url
2. Set transaction hash which will derive public key
'''

ws_url = 'wss://wss.api.moonriver.moonbeam.network'
transaction_hash = 0xf01f8ea90a2e9e54ab61e938c0c5bc9bd296d7ba7730b0a18edab253a5b90927

w3 = web3.Web3(web3.WebsocketProvider(ws_url))
t = w3.eth.getTransaction(transaction_hash)

s=w3.eth.account._keys.Signature(vrs=(to_standard_v(extract_chain_id(t.v)[1]), w3.toInt(t.r), w3.toInt(t.s)))

tt={k:t[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
tt['data']=t.input
tt['chainId']=extract_chain_id(t.v)[0]
ut=serializable_unsigned_transaction_from_dict(tt)

print("It's recovered public key: \n", s.recover_public_key_from_msg_hash(ut.hash()), "\n")
print("It's recovered public key in HEX: \n", s.recover_public_key_from_msg_hash(ut.hash()).to_checksum_address(), "\n")

print("It's publick key from transaction: \n", t['from'], "\n")