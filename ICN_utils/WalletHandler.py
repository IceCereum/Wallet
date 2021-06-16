from pathlib import Path

from web3 import Web3
from eth_account import Account

from .wallet.wallet import Wallet

class WalletHandler(Wallet):
    def __init__(self, name : str, meta_dir : Path):
        Wallet.__init__(self)

        self.wallet_name = name
        self.meta_directory = meta_dir


    def CreateNewWallet(self, password : str):
        # making sure that we have no wallet loaded, otherwise new instance has
        # to be created
        assert self.wallet_name not in                                         \
                        WalletUtils(self.meta_directory).list_wallets(),       \
                            "Wallet: " + self.wallet_name + " already exists"

        Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = Account.create_with_mnemonic()
        encrypted = Account.encrypt(acct._private_key, password)

        self.store_encrypted_data(encrypted_data = encrypted)
        self.address = str(acct._address)

        return acct, mnemonic

    def CreateWalletFromSeed(self, password : str, seed_words : list):
        # making sure that we have no wallet loaded, otherwise new instance has
        # to be created
        assert self.wallet_name not in                                         \
                        WalletUtils(self.meta_directory).list_wallets(),       \
                            "Wallet: " + self.wallet_name + " already exists"

        assert len(seed_words) == 12, "12 exact seed words were not supplied"

        Account.enable_unaudited_hdwallet_features()
        acct = Account.from_mnemonic(" ".join(seed_words))

        encrypted = Account.encrypt(acct._private_key, password)

        self.store_encrypted_data(encrypted_data = encrypted)
        self.address = str(acct._address)

        return True


class WalletUtils:
    def __init__(self, meta_dir : Path):
        self.meta_directory = meta_dir

    def list_wallets(self):
        wallet_dirs = [x for x in self.meta_directory.glob("*") if x.is_dir()]
        wallet_names = []

        for wallet_dir in wallet_dirs:
            name = [x.name.split(".")[0]                                       \
                for x in wallet_dir.glob("*") if x.is_file()]

            assert len(name) == 1,                                             \
                "wallet directory " +wallet_dir+ " has "+ str(name) +          \
                " values, expected only one"

            wallet_names.append(name[0])

        return wallet_names


