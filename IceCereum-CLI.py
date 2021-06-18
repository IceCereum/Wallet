import cmd2, sys, os, requests
from typing import List
from pathlib import Path
from getpass import getpass
from argparse import ArgumentParser, RawTextHelpFormatter
from requests.exceptions import ConnectionError

from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

from ICN_utils.WalletHandler import WalletHandler, WalletUtils
from ICN_utils.generic.error_utils import *

META_DIR = Path("IceCereum-Meta")
# NETWORK = "https://icecereum.icecereal.me:4500"
NETWORK = "http://127.0.0.1:4500"

class IceCereumCLI(cmd2.Cmd):
    """A simple cmd2 application."""

    def __init__(self):
        disable =['do_edit', 'do_ipy', 'do_py', 'do_run_pyscript',
        'do_run_script', 'do__relative_run_script', 'do_shell', 'do_shortcuts']
        for plugin in disable:
            delattr(cmd2.Cmd, plugin)

        super().__init__()
        self.hidden_commands.append('alias')
        self.hidden_commands.append('macro')

        self.prompt = "IceCereum-CLI> "
        self.current_WH = None

    ############################################################################
    ################################ VALIDATORS ################################
    ############################################################################
    def wallet_loaded(function):
        def wrapper(self, *args):
            if self.current_WH == None:
                self.perror("No wallet is currently loaded")
                self.perror("Try using <wallet load> or <wallet create>")
                return None

            return function(self, *args)
        return wrapper

    ############################################################################
    ############################### WALLET UTILS ###############################
    ############################################################################
    wallet_parser = ArgumentParser()
    wp_subparser = wallet_parser.add_subparsers(dest="walletaction")

    wp_create = wp_subparser.add_parser("create")
    wp_create.add_argument("wallet_name", type=str)

    wp_load = wp_subparser.add_parser("load")
    wp_load.add_argument("wallet_name", type=str)

    wp_restore = wp_subparser.add_parser("restore")
    wp_restore.add_argument("wallet_name", type=str)

    wp_delete = wp_subparser.add_parser("delete")
    wp_delete.add_argument("wallet_name", type=str)

    wp_subparser.add_parser("list")

    @cmd2.with_argparser(wallet_parser)
    def do_wallet(self, args):
        """Create a newly generated wallet with a random 12 seed mnemonic

        Usage: CreateNewWallet <wallet_name>
        """
        if args.walletaction == "create":
            self.create_wallet(args.wallet_name)
        elif args.walletaction == "load":
            self.load_wallet(args.wallet_name)
        elif args.walletaction == "restore":
            self.restore_wallet(args.wallet_name)
        elif args.walletaction == "list":
            wallets = WalletUtils(META_DIR).list_wallets()
            self.poutput("List of available wallets:")
            self.poutput(str(wallets))

        return None


    def create_wallet(self, wallet_name : str):
        if wallet_name in WalletUtils(META_DIR).list_wallets():
            self.perror("Wallet " + wallet_name + " already exists")
            self.perror("Choose a different name")
            return

        self.poutput("You are about to see your 12 word seed phrase.")
        self.poutput("Make sure you have a piece of paper to write it down.")
        self.poutput("The screen will be cleared once you have finished "      \
                     "writing down the words and you will NEVER see them "     \
                     "again.")

        while True:
            passwd_orig   = getpass("Enter a password for your wallet: ")
            passwd_repeat = getpass("Enter your password again: ")

            if passwd_orig == passwd_repeat:
                break
            self.perror("Your passwords did not match! Try again")

        del passwd_repeat

        wh = WalletHandler(name = wallet_name, meta_dir = META_DIR)
        _, mnemonic = wh.CreateNewWallet(password = passwd_orig)

        del passwd_orig

        ### SEED PHRASE ###
        unit_words = mnemonic.split(" ")

        self.poutput("\nHere are your words:")

        for index, word in enumerate(unit_words):
            self.poutput("%d. %s (Hit Enter)" % (index + 1, word))
            _ = input()

        confirm = input("Have you noted down all 12 words? The screen will "   \
            "clear after this (yes/no): ")

        while (confirm != "yes"):
            confirm = input("Type yes to continue (yes/no): ")

        del mnemonic, unit_words
        os.system('cls' if os.name=='nt' else 'clear')

        self.current_WH = wh

        self.poutput("Your wallet: %s has been created!" % wallet_name)
        self.poutput("Wallet Address: %s" % self.current_WH.address)
        self.poutput("\nDo NOT share the 12 words or the wallet file")

        return None

    def load_wallet(self, wallet_name : str):
        wallets = WalletUtils(META_DIR).list_wallets()

        if wallet_name not in wallets:
            self.perror("Wallet " + wallet_name + " doesn't exist")
            self.poutput("List of available wallets:")
            self.poutput(str(wallets))
            return None

        wh = WalletHandler(name = wallet_name, meta_dir = META_DIR)
        self.current_WH = wh

        self.poutput("Wallet " + wallet_name + " loaded")

        return None

    def restore_wallet(self, wallet_name : str):
        if wallet_name in WalletUtils(META_DIR).list_wallets():
            self.perror("Wallet " + wallet_name + " already exists")
            self.perror("Choose a different name")
            return None

        self.poutput("Enter your words (lowercase)")
        words = []
        for i in range(12):
            word = input("Enter word " + str(i+1) + ": ")
            words.append(word.lower())

        os.system('cls' if os.name=='nt' else 'clear')

        while True:
            passwd_orig   = getpass("Enter a password for your wallet: ")
            passwd_repeat = getpass("Enter your password again: ")

            if passwd_orig == passwd_repeat:
                break
            self.perror("Your passwords did not match! Try again")

        wh = WalletHandler(name = wallet_name, meta_dir = META_DIR)
        wh.CreateWalletFromSeed(passwd_orig, words)

        del passwd_orig, passwd_repeat, words, word

        self.current_WH = wh
        self.poutput("Wallet: %s has been restored!" % wallet_name)
        self.poutput("Wallet Address: %s" % self.current_WH.address)
        self.poutput("If this address is not the same as your previous address"\
            ", you may have entered the words incorrectly or out of order.")

        return None

    # TODO: deletewallet

    ############################################################################
    ############################## ACCOUNT TOOLS ###############################
    ############################################################################
    @cmd2.with_argument_list
    @wallet_loaded
    def do_address(self, args):
        self.poutput("Address - Wallet %s: %s"                                 \
            % (self.current_WH.wallet_name, self.current_WH.address))

    @cmd2.with_argument_list
    @wallet_loaded
    def do_balance(self, args):
        init_json = {
            "sendr_addr" : self.current_WH.address
        }

        init_response = requests.get(NETWORK + "/get-balance", json = init_json)
        response = init_response.json()

        if response["success"] == False:
            errormessage(
                "GET NETWORK/get-balance returned",
                response["message"],
                escalated=True
            )
            return None

        if response["exists"] == False:
            self.poutput("The requested address has no transactions on the"    \
                "IceCereum Network")
            return None

        self.poutput("Balance : %f" % float(response["balance"]))

        return None

    # transactions_parser = ArgumentParser()
    # transactions_parser.add_argument("-nsync", "--no-sync", action="store_true", required=False)


    sync_parser = ArgumentParser()
    sync_parser.add_argument("-nmsg", "--no-message", action="store_true", required=False)

    @cmd2.with_argparser(sync_parser)
    @wallet_loaded
    def do_sync(self, args):
        init_json = {
            "address" : self.current_WH.address
        }

        init_response = None
        try:
            init_response = requests.get(NETWORK + "/get-transactions",
                                                            json = init_json)
        except ConnectionError as e:
            errormessage(
                self, "Unable to connect to the IceCereum Network.",
                "> Do you have an active internet connection?",
                "> Could you check if the IceCereum Network is down?",
                exception=e)
            return None

        init_response_json = init_response.json()
        if init_response_json["success"] == False:
            errormessage(
                self, "GET NETWORK/get-transactions returned:",
                init_response_json["message"], "Init JSON",
                [init_json])
            return None

        if init_response_json["exists"] == False:
            self.poutput("This wallet's address does not exist on the "        \
                            "IceCereum Network.")
            return None

        send_tx = self.current_WH.get_sendfile()
        recv_tx = self.current_WH.get_receivedfile()

        server_send_tx = {}
        server_recv_tx = {}

        for server_tx in init_response_json["transactions"]:
            tx_data = init_response_json["transactions"][server_tx]
            if tx_data["type"] == "send":
                server_send_tx[len(server_send_tx)] = tx_data
            elif tx_data["type"] == "receive":
                server_recv_tx[len(server_recv_tx)] = tx_data

        # At the moment, we assume that a person has a wallet only on one device
        # and they don't use the same account on other devices. So I'm not
        # syncing send (because of server received timestamps and client sent
        # timestamps)
        if len(server_recv_tx) == len(recv_tx):
            self.poutput("Sync complete! No new transactions were added")
            return None

        for i in range(len(recv_tx), len(server_recv_tx)):
            sender = str(server_recv_tx[i]["sendr_addr"])
            amount = str(server_recv_tx[i]["value"])
            mining_fee = str(server_recv_tx[i]["mining_fee"])
            total_amount = str(server_recv_tx[i]["final_value"])
            in_txpool = str(server_recv_tx[i]["in_txpool"])

            msg = ""
            if not args.no_message:
                self.poutput("Received Transaction:")
                self.poutput("  sender: %s" % sender)
                self.poutput("  amount: %s" % amount)
                self.poutput("  mining_fee: %s" % mining_fee)
                self.poutput("  total_amount: %s" % total_amount)
                self.poutput("  in_txpool: %s" % in_txpool)

                if sender == "IceCereum-Rewards":
                    msg = "IceCereum Rewards"
                    self.poutput("  Congratulations! You got a reward!")
                else:
                    msg = input("  Enter message (blank for no message): ")

            self.current_WH.log_recvfile(
                sender = sender,
                amount = amount,
                mining_fee = mining_fee,
                total_amount = total_amount,
                message = msg
            )

        self.poutput("Sync complete!")
        return None


    ############################################################################
    ############################### NICK UTILS #################################
    ############################################################################
    nick_parser = ArgumentParser()
    nick_subparser = nick_parser.add_subparsers(dest="nickaction")

    nick_create = nick_subparser.add_parser("create", aliases=["add"])
    nick_create.add_argument("name", type=str)
    nick_create.add_argument("address", type=str)

    nick_delete = nick_subparser.add_parser("delete", aliases=["del"])
    nick_delete.add_argument("name", type=str)

    nick_info = nick_subparser.add_parser("info")
    nick_info.add_argument("name", type=str)

    nick_subparser.add_parser("list")

    @cmd2.with_argparser(nick_parser)
    @wallet_loaded
    def do_nick(self, args):
        if args.nickaction == "create" or args.nickaction == "add":
            self.nick_create(args.name, args.address)
        elif args.nickaction == "delete":
            self.nick_delete(args.name)
        elif args.nickaction == "info":
            self.nick_info(args.name)
        elif args.nickaction == "list":
            self.nick_list()

        return None

    def nick_create(self, name : str, addr : str):
        retval = self.current_WH.CreateNick(name, addr)
        if retval == -1:
            self.perror("Nick already exists")
            self.poutput("Choose a different name")
            return None
        elif retval == -2:
            self.perror("Supplied address is not a valid address")
            self.poutput("Verify that the address you supplied is correct")
            return None
        elif retval == -3:
            self.perror("Supplied nick is an IceCereum address")
            self.poutput("Uh... Did you get your order mixed up?")
            self.poutput("It's nick create <nick_name> <address>")
            self.poutput("You can't enter an address for <nick_name>")
            self.poutput("That would ... break logic")
            return None
        elif retval == -4:
            self.perror("Supplied address is your address")
            self.poutput("Are you trying to nick your own self?")
            self.poutput("Yeah ... we can't let that happen now, can we?")
            return None
        elif retval == 1:
            self.poutput("Nick created!")
            return None

    def nick_delete(self, name : str):
        nick, addr = self.current_WH.DeleteNick(name)
        if nick == -1:
            self.perror("Nick does not exist")
            self.poutput("Try <nick list> to get a list of nicks")
            return None
        else:
            self.poutput("Nick: %s with Address: %s deleted" % (nick, addr))
            return None

    def nick_info(self, name : str):
        nicks = self.current_WH.ListNicks()
        if name not in nicks:
            self.perror("Nick does not exist")
            self.poutput("Try <nick list> to get a list of nicks")
            return None
        else:
            self.poutput("Nick Info - Name: %s - Address: %s" %                \
                                                (name, nicks[name]))
            return None

    def nick_list(self):
        nicks = self.current_WH.ListNicks()
        if len(nicks) == 0:
            self.poutput("There are no nicks. To create one, try <nick create>")

        for nick in nicks:
            print ("Nick: %s - Address: %s" % (nick, nicks[nick]))

        return None


    ############################################################################
    ############################## TRANSFER UTILS ##############################
    ############################################################################
    """
        This has to adhere to the IceCereum protocol which runs (from the
        client) as:

        NOTE: This has to be a requests.session because the server sends some
              session cookies to "store state" between the calls

        1. resp = GET (/transfer-funds, json({'sendr_addr' : sender address})

        resp (json) contains a one_time_nonce, which has to be included in the
        signed message when POSTed; resp (json) also contains mining fees;
        
        2. message_to_sign = "{sendr_addr}{recvr_addr}{value}{one_time_nonce}"

        3. signed_message = sign_message(message_to_sign, private_key)

        4. POST_JSON = {
            "sendr_addr" : sender's address
            "recvr_addr" : receiver's address
            "value" : amount to transfer
            "one_time_nonce" : nonce from the respone of GET
            "skscript" : signed_message (without nonce)
            "skscript_nonce" : signed_message (with nonce)
        }

        5. POST (/transfer-funds, json(POST_JSON))
    """
    transfer_parser = ArgumentParser()
    transfer_parser.add_argument("-to", "--to-address", type=str, required=False)
    transfer_parser.add_argument("-a", "--amount", type=float, required=False)
    transfer_parser.add_argument("-msg", "--message", type=str, required=False)

    @cmd2.with_argparser(transfer_parser)
    @wallet_loaded
    def do_transfer(self, *args):
        args = args[0]

        to_address = None
        amount = None
        message = None

        if args.to_address and (args.amount is None):
            self.perror("Missing arguments!")
            self.perror("Usage: transfer --to-address <to_addr> --amount "     \
                        "<amount> --message <message>")
            self.perror("or simply type transfer to enter interactive mode")

        elif args.to_address:
            to_address = args.to_address
            amount = args.amount
            message = args.message or ""

        else:
            to_address = input("Send To (enter an alias / valid address): ")
            amount = input("Enter Amount to Send (minimum 0.01): ")
            message = input("Enter message (for transaction history): ")

        stat, v_args = self.validate_transfer_args(to_address, amount, message)
        if stat != 1:
            return None

        to_address = v_args[0]
        amount = v_args[1]
        message = v_args[2]

        # Refer to NOTE of the protocol described above
        session = requests.Session()

        ### Step 1 of protocol ###
        init_json = {
            "sendr_addr" : self.current_WH.address
        }

        init_response = None
        try:
            init_response = session.get(NETWORK + "/transfer-funds",
                                                            json = init_json)
        except ConnectionError as e:
            errormessage(
                self, "Unable to connect to the IceCereum Network.",
                "> Do you have an active internet connection?",
                "> Could you check if the IceCereum Network is down?",
                exception=e)
            return None

        init_response_json = init_response.json()

        if init_response_json["success"] == False:
            errormessage(
                self, "GET NETWORK/transfer-funds returned:",
                init_response_json["message"], "Command params",
                [to_address, amount, message])
            return None

        # Confirming whether the user *really* wants to 
        one_time_nonce = init_response_json["one_time_nonce"]
        mining_fees = float(init_response_json["mining_fees"])

        total_amount = amount + mining_fees

        self.poutput("The current IceCereum Network mining fees are: " +       \
                                                               str(mining_fees))
        self.poutput("The total amount transferred will be %f + %f = %f"       \
            % (amount, mining_fees, total_amount))
        self.poutput("Type yes/no continue transferring: %f" % total_amount)

        confirm = input()
        if confirm.lower() not in ["yes"]:
            self.poutput("Transaction cancelled")
            return None

        # This corresponds to step 4
        transaction_json = {
            "sendr_addr" : self.current_WH.address,
            "recvr_addr" : to_address,
            "value" : total_amount,
            "one_time_nonce" : one_time_nonce
        }

        ### Step 2 of protocol ###
        message_to_sign_no_nonce = "{sendr_addr}{recvr_addr}{value}"           \
            .format(
                sendr_addr = transaction_json["sendr_addr"],
                recvr_addr = transaction_json["recvr_addr"],
                value = transaction_json["value"],
                nonce = transaction_json["one_time_nonce"]
            )
        message_to_sign_nonce = "{sendr_addr}{recvr_addr}{value}{nonce}"       \
            .format(
                sendr_addr = transaction_json["sendr_addr"],
                recvr_addr = transaction_json["recvr_addr"],
                value = transaction_json["value"],
                nonce = transaction_json["one_time_nonce"]
            )

        to_decrypt = self.current_WH.get_raw_data()

        decrypted_account = None
        while True:
            passwd = getpass("Password for Wallet " +                          \
                                self.current_WH.wallet_name + ": ")
            try:
                decrypted_account = Account.decrypt(to_decrypt, passwd)
                break
            except ValueError:
                self.perror("The entered password is wrong. Try again")

        ### Step 3 of protocol ###
        msg = encode_defunct(text = message_to_sign_no_nonce)
        signature_no_nonce = Account.                                          \
                            sign_message(msg, decrypted_account.hex()).signature
        msg = encode_defunct(text = message_to_sign_nonce)
        signature_nonce = Account.                                             \
                            sign_message(msg, decrypted_account.hex()).signature

        del passwd, decrypted_account

        ### Finishing Step 4 of protocol ###
        # Storing generated signature
        transaction_json["skscript"] = signature_no_nonce.hex()
        transaction_json["skscript_nonce"] = signature_nonce.hex()

        ### Step 5 of protocol ###
        transaction_response = None
        try:
            transaction_response =                                             \
                session.post(NETWORK+"/transfer-funds", json=transaction_json)
        except ConnectionError as e:
            errormessage(
                self, "POST NETWORK/transfer-funds was unable to connect\n",
                "Unable to connect to the IceCereum Network.",
                "> Do you have an active internet connection?",
                "> Could you check if the IceCereum Network is down?",
                exception=e)
            return None

        transaction_response = transaction_response.json()

        if transaction_response["success"] == False:
            print (self.current_WH.address, transaction_json["sendr_addr"])
            errormessage(self,
                "POST NETWORK/transfer-funds returned",
                transaction_response["message"],
                escalted=True)
            return None

        else:
            self.poutput("Transaction added to TXPOOL!")

        self.current_WH.log_sendfile(
            to = to_address,
            amount = amount,
            mining_fee = mining_fees,
            total_amount = total_amount,
            message = message
        )

        return None


    def validate_transfer_args(self, to_address, amount, message):
        nicks = self.current_WH.ListNicks()
        if to_address in nicks:
            to_address = nicks[to_address]

        if not Web3().isAddress(to_address):
            self.perror("Invalid Address Supplied!")
            self.poutput("The TO_ADDRESS provided is not a valid IceCereum "   \
                "Address. If your TO_ADDRESS is a nick, you may have an "      \
                "invalid address in your nicks file. Try <nick list> to get "  \
                "a list of all your nicks and check the address of the nick "  \
                "you supplied")
            return (-1, ())

        try:
            amount = float(amount)
            if amount < 0.01:
                raise AssertionError
        except ValueError:
            self.perror("Invalid Amount! The amount entered is not a number.")
            return (-1, ())
        except AssertionError:
            self.perror("The minimum transferable amount is 0.01")
            return (-1, ())

        return (1, (to_address, amount, message))


if __name__ == '__main__':
    c = IceCereumCLI()
    sys.exit(c.cmdloop())
    # wu = WalletUtils(meta_dir = META_DIR)
    # wu.list_wallets()