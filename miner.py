import os
import sys
import time
import ecdsa
import random
import base58
import hashlib
import binascii
from concurrent.futures import ThreadPoolExecutor
import secrets
import logging

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[0m[\x1b[38;2;63;63;63m%(asctime)s\x1b[0m] %(message)s",
    datefmt="%H:%M:%S"
)

class BitcoinAddress:
    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = self.private_key_to_public_key(private_key)
        self.address = self.public_key_to_address(self.public_key)

    def private_key_to_public_key(self, private_key):
        sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
        return "04" + binascii.hexlify(sign.verifying_key.to_string()).decode("utf-8")

    def public_key_to_address(self, public_key):
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        count = 0
        var = hashlib.new("ripemd160")
        var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
        doublehash = hashlib.sha256(
            hashlib.sha256(binascii.unhexlify(("00" + var.hexdigest()).encode())).digest()
        ).hexdigest()
        address = "00" + var.hexdigest() + doublehash[0:8]
        for char in address:
            if char != "0":
                break
            count += 1
        count = count // 2
        n = int(address, 16)
        output = []
        while n > 0:
            n, remainder = divmod(n, 58)
            output.append(alphabet[remainder])
        while count > 0:
            output.append(alphabet[0])
            count -= 1
        return "".join(output[::-1])

class Bitcoin:
    def __init__(self):
        self.checked = 0
        self.profit = 0

        if sys.platform != "win32":
            os.system("clear")
        else:
            os.system("cls")

    def title_task(self):
        while True:
            time.sleep(0.08)
            os.system("title [BTC] Profit: %s ^| Checked: %s" % (self.profit, self.checked))

    def generate_private_key(self):
        return binascii.hexlify(secrets.token_bytes(32)).decode("utf-8")

    def task(self, hit=False):
        private_key = self.generate_private_key()
        bitcoin_address = BitcoinAddress(private_key)

        self.checked += 1
        if len(bitcoin_address.address) == 33:
            bitcoin_address.address += " "

        if hit:
            balance = random.uniform(0.0005, 0.9)
            self.profit += balance
            logging.info(f"{bitcoin_address.address} (\x1b[38;2;63;63;63m{balance} BTC\x1b[0m)")
            logging.info(
                f"\x1b[32mSuccessfully found address\x1b[0m, sending \x1b[32m{self.profit}\x1b[0m BTC to \x1b[38;2;63;63;63m{self.address}\x1b[0m."
            )
            logging.info("Continuing in \x1b[38;2;63;63;63m15\x1b[0m seconds.")
            time.sleep(15)
        else:
            logging.info(f"{bitcoin_address.address} (\x1b[38;2;63;63;63m0 BTC\x1b[0m)")

    def run(self):
        self.address = input("\x1b[0m[\x1b[38;2;63;63;63m~\x1b[0m] Address\x1b[38;2;63;63;63m>\x1b[0m ")
        self.hit_at = int(input("\x1b[0m[\x1b[38;2;63;63;63m~\x1b[0m] Hit at\x1b[38;2;63;63;63m>\x1b[0m "))
        print()

        with ThreadPoolExecutor(max_workers=100_000) as pool:
            pool.submit(self.title_task)
            for x in range(1_000_000):
                try:
                    self.task()
                    if not self.checked % self.hit_at:
                        self.task(True)
                        # time.sleep(0.1)
                except Exception as e:
                    logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    client = Bitcoin()
    client.run()
