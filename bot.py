import requests
import tweepy
import time
import os

# Twitter API keys from environment variables
TW_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
TW_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TW_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

# Etherscan API key
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

# Replace these two Ethereum addresses with the ones you want to track:
ADDRESSES = {
    'wallet1': '0xeD68CF204135a19c8d2eb072eaf7398bd3be1eBE',
    'wallet2': '0xBc1D9D88b29E2f11B5Babf23f106Ef3368618963',
}

auth = tweepy.OAuth1UserHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET, TW_ACCESS_TOKEN, TW_ACCESS_SECRET)
api = tweepy.API(auth)

last_tx = {}

def get_latest_tx(address):
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&sort=desc&apikey={ETHERSCAN_API_KEY}'
    r = requests.get(url)
    data = r.json()
    if data['status'] == '1' and data['result']:
        return data['result'][0]
    return None

while True:
    for name, address in ADDRESSES.items():
        tx = get_latest_tx(address)
        if not tx:
            continue
        tx_hash = tx['hash']
        if last_tx.get(address) != tx_hash:
            eth_value = int(tx['value']) / 1e18
            to_addr = tx['to']
            from_addr = tx['from']
            tweet = (
                f"🔔 New transaction from {name}:\n"
                f"💸 {eth_value:.4f} ETH\n"
                f"📤 From: {from_addr[:6]}... → 📥 To: {to_addr[:6]}...\n"
                f"🔗 https://etherscan.io/tx/{tx_hash}"
            )
            api.update_status(tweet)
            last_tx[address] = tx_hash
    time.sleep(60)
