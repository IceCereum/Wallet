# This is the ultra-simple, Explain-Like-I'm-5 instructions

### If you're on windows:

- Download the file [here](https://github.com/IceCereum/Wallet/releases). You
have to click on the Assets button to reveal the IceCereum-CLIv.1.0-beta.exe
program that should be downloaded.
- Create a folder on your computer anywhere you want and place this program
inside that folder.
- Double click on it to run the program

### If you're on MacOS / Linux:

- Make sure you have Python3 installed - check that out
[here](https://installpython3.com/mac/)
- Go back to the [original page](https://github.com/IceCereum/Wallet/) and where
you see the green button that says Code, click on that and choose download zip
and extract it.
- Open terminal and [`cd`](https://www.macworld.com/article/221277/master-the-command-line-navigating-files-and-folders.html)
to the directory where you extracted the zip.
- Type `python3 IceCereum-CLI.py` to run the program

## Create a wallet, address, transfer funds

Create your wallet by typing `wallet create wallet_name`, replacing wallet_name
with a wallet name of your choice. You will be shown 12 words - write them down
on a piece of paper and don't reveal it to anyone. Every time you run the
program you should load the wallet by using `wallet load wallet_name`.

Enter a password for your wallet. DON'T enter your normal password; enter a
generic password like `password`. In case you forget this password, you can
restore the password at any time using the 12 words you just noted.

Once you're done, type `address` to reveal your address. You can send this
address to anyone for them to send funds to you. You can also type `balance` to
reveal your balance. It should be 0 by default as you have no coins that entered
your account.

You can get the addresses of other people by asking them their address and
saving it in nicks instead of remembering the huge address. For example:
`nick create icecereal 0x.....long address.....` stores my address in a nick
called icecereal.

To transfer funds, you must first have funds. After asking someone (mostly me)
for funds, you can type `sync` to check if you received any new funds. You will
have to enter a message - this is for the future you to remember what this
transaction was for. Once you `sync` and if you see new incoming transactions,
that means you received funds. Type `balance` to check your balance.

To transfer funds, type `transfer`. You will be asked 3 questions: To, Amount
and Message. The To field can be an entire address or a nick you assigned two
paragraphs ago. The amount will have to be a number. The message is for the
future you to remember what this transaction was for. You will be shown what the
network's current mining fee is - this is the amount you have to pay to the
network to process the transaction. If you are comfortable with the number, type
`yes` and enter your password. Let the other person know you sent them coins and
they can check it up with `sync`.