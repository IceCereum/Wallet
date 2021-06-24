# IceCereum Wallet

The purpose of this wallet is to connect to the IceCereum Network and be able to
transfer accounts on your behalf. This wallet is likely to remain stable as the
basic functionality of interacting with the IceCereum Network are complete.
However, in the event of a new update being available, the wallet should notify
you that there is a new update.

If you want a barebones and very simple instructions, feel free to check out
[The ELI5 instructions](./eli5-instructions.md)

## Installation Instructions

### Windows

If you have windows, you can install the latest release from
[releases](https://github.com/IceCereum/Wallet/releases). The OS may ask you to
be wary of downloading a random exe from off the internet, but eh, you trust me
...right? If you don't, try running from source as outlined below.

### MacOS / Linux / Running from Source

For MacOS and Linux, I cannot create an executable file because of limitations
of PyInstaller, the package that is used to generate executables. To do run it
from source, make sure you have Python3.8+ installed. You also need to have
`python3-dev` installed if you're on Linux (found 
[here](https://stackoverflow.com/a/21530768)

```sh
python3 --version # for MacOS / Linux
py --version # for Windows
```

Next, either:

- clone this repository
- download the code as a zip, extract it and cd into that folder

```sh
git clone https://github.com/IceCereum/Wallet.git
```

You can choose to set up a virtual environment or you can choose to install
requirements straight away

```sh
virtualenv icecereum
source icecereum/bin/activate
python3 -m pip install -r requirements.txt # for MacOS / Linux
py -m pip install -r requirements.txt # for Windows
```

Now, you should be ready to run the program

```sh
python3 IceCereum-CLI.py # for MacOS / Linux
py IceCereum-CLI.py # for Windows
```

## Usage

To understand the general program capabilites along with what the IceCereum
Network is, type `info` in your CLI. This should explain how to use the program
for the first time. In case you want to be reminded of how to use the program,
type `shortinfo` to get a quick summary. Briefly, the functionalities of the
program are:

### Information

This contains `info` and `shortinfo`. They have no arguments.

### Wallet

This contains all the handling capabilities of interacting with your encrypted
wallet.

```
wallet create <wallet_name>
wallet load <wallet_name>
wallet list
wallet restore <wallet_name>
```

When you create your wallet, you will be asked to enter a password. Enter some
generic password and NOT your usual password. This program hasn't been made with
keeping Side-Channel attacks in mind and thus if someone attempts to get data
from your cache, RAM, storage or whatever, they may be able to get your data.
You'll be soon shown 12 random words which will be **NEVER** shown again. These
12 words are now your seed. This seed is the most important thing about your
wallet as it can restore it in case you forget your password. **NEVER** share
this seed with anyone and **NEVER** note it down digitally. It is always
recommended to store your seed on a piece of paper and keep that piece of paper
safe.

Once you create your wallet after entering your password and noting down your
seed, you will see a folder generated called `IceCereum-Meta/`. This program and
the newly generated folder must always be in the same directory for you to use
your wallet. When you close the program and re-open it, you should use 
`wallet load <wallet_name>` to access your wallet again. In case you forgot your
wallet name, type `wallet list` to list all the wallets you have.

In the event that you lose your wallet file or forget your password, it is
possible to restore it using `wallet restore <wallet_name>`. In that case, you
will be asked to enter another password and re-enter the 12 words that you were
shown at the time of creating the wallet. Enter the words in the originally
shown order.

### Account Stats

`address` shows you your loaded wallet address. `balance` shows you your loaded
wallet's balance on the network. `transactions` shows a list of all the
transactions that have been locally recorded. This will not sync transactions
with the network. In case you wish to see incoming transactions that haven't
been stored locally, type `sync` and you will have to enter a message for every
new transaction you get (leave it blank for no message).

### Transferring funds

Now that you have a wallet, you may want to transfer some funds. There are two
ways that this can be done. An interactive way and a non-interactive way. For
the interactive way, you can type transfer and the program will accordingly
prompt you for the address to send coins to, the amount to send and a message to
remind you what this transaction is for (the message is stored on your computer
and not sent to the network). If you don't want to be prompted, you can do
`transfer -to <to_address> -a <amount> -msg <message>` to achieve just the same.

Once you finish entering these details, you will be shown the current network's
mining fee and be accordingly asked whether you are okay with sending that
amount. Every 3 hours, the mining fee of the network is revised based off of the
activity of the previous three hours. If there were a lot of transactions, the
mining fee would be high for the next three hours. Similarly, if there were only
a few transactions, the mining fee would be low.

If you are okay to transfer the amount + mining fee, you will be asked to enter
your wallet password in order to transfer the funds. If the transfer was
successful, you should see "Transaction added to TXPOOL" as the message. This
means that the transfer has been successful, but not yet added to the
blockchain. Every three hours, transactions from the TXPOOL will be added to the
blockchain.

To make the receiver realise that you transferred the funds, ask them to `sync`
to see their transactions. They should be able to see a new incoming transaction
that corresponds to what you just sent.

### Nicks

To enter a 42 character long address can be hard every time you want to
transfer funds. This program has the option of creating nicknames - aliases that
store addresses under names. Instead of typing out:

`transfer -to 0x...long_address... -a 10.5 -msg "some message"`,

you can do:

`transfer -to <name> -a 10.5 -msg "some message"`

```sh
nick create <name> 0x...long_address...
nick list
nick info <name>
nick delete <name>
```

Create a nick using `nick create`; list all the nicks you have stored by typing
`nick list`; to get a particular nick, use `nick info`; to delete a nick use
`nick delete`.

### Command help

If you need any help about a command, type `help <command_name>` for the
description and usage to show up

## IceCereum Rewards

Occasionally, you may see you received funds from `IceCereum-Rewards`. Those are
rewards for transferring funds to someone. To read more about the workings of
the IceCereum Network, read [protocol](https://github.com/IceCereum/Protocol).

## I Created My Wallet. Now What?

Now that you created your wallet, it's time for you to receive some funds.
Unfortunately since this is a *private* cryptocurrency, you can't really buy
these coins anywhere. This cryptocurrency was created as meme and is intended
to be only "used" between my friends and I. If you know me and want some
IceCereums, shoot me an email and I'll transfer some to you. Otherwise if you
know someone on the network, you can ask them to transfer coins to you.

## I encountered a bug / Something went wrong / Help

In case you find a bug or something goes wrong, first type `set debug true` and
repeat your command. Copy that entire error message and
[create an issue](https://github.com/IceCereum/Wallet/issues). That way I'll
respond to you (hopefully) to fix out the bug.

If you need help, make sure you've read this README and then ask a question by
raising an issue. If something is unclear, I'll undoubtedly update this README
so that others don't face issues. But don't ask for help without reading this
README because that's just very annoying.
