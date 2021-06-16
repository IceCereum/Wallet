from pathlib import Path
from json import load, dump, dumps

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
            return self._address

    @address.setter
    def address(self, address : str):
        assert Web3().isAddress(address) == True,                              \
                        "address supplied is not valid"
        if address.startswith("0x"):
            self._address = address
        else:
            self._address = "0x" + address

    @property
    def generic_path(self):
        p = Path(self.meta_directory / self.wallet_name)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def hist_path(self):
        h = self.generic_path / Path(self.wallet_name + "-History/")
        h.mkdir(parents=True, exist_ok=True)
        return h

    @property
    def aliasfile_path(self):
        return self.generic_path /                                             \
            Path(self.wallet_name + ".IceCereum-Aliases.json")

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

    def log_histfile(self, **kwargs):
        n_files = len(list(self.hist_path.glob('*')))
        filename = self.hist_path / Path(str(n_files).zfill(3) + ".json")

        output = {
            "time" : time_now()
        }

        for key in kwargs:
            output[key] = kwargs.get(key)

        with open(filename, 'w') as F:
            dump(output, F, indent=2)

        return None
