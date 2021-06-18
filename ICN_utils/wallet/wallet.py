from pathlib import Path
from json import load, dump, dumps, JSONDecodeError

from web3 import Web3
from eth_account import Account

from ..generic.time_utils import *

class Wallet:
    def __init__(self):
        self.wallet_name = None
        self.meta_directory = None

    @property
    def address(self):
        try:
            return self._address
        except:
            self._address = "0x" + self.get_raw_data()["address"]
            return self._address.lower()

    @address.setter
    def address(self, address : str):
        assert Web3().isAddress(address) == True,                              \
                        "address supplied is not valid"
        if address.startswith("0x"):
            self._address = address.lower()
        else:
            self._address = "0x" + address.lower()

    @property
    def generic_path(self):
        p = Path(self.meta_directory / self.wallet_name)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def history_sendfile_path(self):
        h = self.generic_path / Path(self.wallet_name + "-tx-outgoing.json")
        return h

    @property
    def history_receivedfile_path(self):
        h = self.generic_path / Path(self.wallet_name + "-tx-incoming.json")
        return h

    @property
    def nickfile_path(self):
        return self.generic_path /                                             \
            Path(self.wallet_name + ".IceCereum-Nicks.json")

    @property
    def walletfile_path(self):
        return self.generic_path /                                             \
            Path(self.wallet_name + ".IceCereum-Wallet.json")


    def get_raw_data(self):
        with open(self.walletfile_path, 'r') as F:
            self.to_decrypt = load(F)
        return self.to_decrypt

    def store_encrypted_data(self, encrypted_data : str):
        with open(self.walletfile_path, 'w') as F:
            F.write(dumps(encrypted_data))
        return True

    def log_sendfile(self, **kwargs):
        send_json = None
        try:
            with open(self.history_sendfile_path, 'r') as F:
                send_json = load(F)
        except FileNotFoundError:
            self.history_sendfile_path.touch()
            send_json = {}
        except JSONDecodeError:
            send_json =  {}

        index = len(send_json)

        output = {
            "time" : time_now()
        }

        for key in kwargs:
            output[key] = kwargs.get(key)

        send_json[index] = output

        with open(self.history_sendfile_path, 'w') as F:
            dump(send_json, F, indent=2)

        return

    def log_recvfile(self, **kwargs):
        recv_json = None
        try:
            with open(self.history_receivedfile_path, 'r') as F:
                recv_json = load(F)
        except FileNotFoundError:
            self.history_receivedfile_path.touch()
            recv_json = {}
        except JSONDecodeError:
            recv_json =  {}

        index = len(recv_json)

        output = {
            "time" : time_now()
        }

        for key in kwargs:
            output[key] = kwargs.get(key)

        recv_json[index] = output

        with open(self.history_receivedfile_path, 'w') as F:
            dump(recv_json, F, indent=2)

        return

    def get_sendfile(self):
        try:
            with open(self.history_sendfile_path, 'r') as F:
                send_json = load(F)
        except FileNotFoundError:
            self.history_sendfile_path.touch()
            send_json = {}
        except JSONDecodeError:
            send_json =  {}

        return send_json

    def get_receivedfile(self):
        try:
            with open(self.history_receivedfile_path, 'r') as F:
                recv_json = load(F)
        except FileNotFoundError:
            self.history_receivedfile_path.touch()
            recv_json = {}
        except JSONDecodeError:
            recv_json =  {}

        return recv_json