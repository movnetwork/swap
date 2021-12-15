<img align="right" height="132" src="https://raw.githubusercontent.com/meherett/swap/master/docs/static/svg/readme/swap.svg">

# Swap

[![Build Status](https://travis-ci.com/movnetwork/swap.svg?branch=master)](https://travis-ci.com/movnetwork/swap?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/swap.svg?color=blue)](https://pypi.org/project/swap)
[![Documentation Status](https://readthedocs.org/projects/swap/badge/?version=master)](https://swap.readthedocs.io)
[![PyPI License](https://img.shields.io/pypi/l/swap?color=black)](https://pypi.org/project/swap)
[![PyPI Python Version](https://img.shields.io/pypi/pyversions/swap.svg)](https://pypi.org/project/swap)
[![Coverage Status](https://coveralls.io/repos/github/movnetwork/swap/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/movnetwork/swap?branch=master)

A Python library for Cross-chain atomic swap between the networks of two cryptocurrencies. 
Cross-chain atomic swap is the cheapest and most secured by cryptographic proof to swap cryptocurrencies. 
It’s a brand new decentralized payment environment based on Hash Time Lock Contracts (HTLCs) protocol.

## Available Cryptocurrencies, Assets & Tokens

You can swap the following available cryptocurrencies:

| Cryptocurrencies                                                                                                                                                                                                                                               | Networks                                            |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------: |
| <img align="left" height="25" src="https://raw.githubusercontent.com/movnetwork/swap/master/docs/static/svg/readme/bitcoin.svg"> [Bitcoin](https://github.com/bitcoin/bitcoin) `BTC`                                                                           | `mainnet`, `testnet`                                |
| <img align="left" height="25" src="https://raw.githubusercontent.com/movnetwork/swap/master/docs/static/svg/readme/bytom.svg"> [Bytom v1.0](https://github.com/bytom/bytom) `BTM` - [More Assets](https://classic.blockmeta.com/assets)                        | `mainnet`, `solonet`, `testnet`                     |
| <img align="left" height="25" src="https://raw.githubusercontent.com/movnetwork/swap/master/docs/static/svg/readme/ethereum.svg"> [Ethereum](https://github.com/ethereum/go-ethereum) `ETH`, `ERC20` - [More Tokens](https://etherscan.io/tokens)              | `mainnet`, `ropsten`, `kovan`, `rinkeby`, `testnet` |
| <img align="left" height="25" src="https://raw.githubusercontent.com/movnetwork/swap/master/docs/static/svg/readme/vapor.svg"> [Vapor](https://github.com/bytom/vapor) `BTM` - [More Assets](https://vapor.blockmeta.com/assets)                               | `mainnet`, `solonet`, `testnet`                     |
| <img align="left" height="25" src="https://raw.githubusercontent.com/movnetwork/swap/master/docs/static/svg/readme/xinfin.svg"> [XinFin](https://github.com/XinFinOrg/XDPoSChain) `XDC`, `XRC20` - [More Tokens](https://explorer.xinfin.network/tokens/xrc20) | `mainnet`, `apothem`, `testnet`                     |

## What is a HTLC?

A Hash Time Lock contract (HTLC) is essentially a type of payment in which two people
agree to a financial arrangement where one party will pay the other party a certain
amount of cryptocurrencies, such as Bitcoin or Bytom assets. However, because these
contracts are Time Locked, the receiving party only has a certain amount of time to
accept the payment, otherwise the money can be returned to the sender.

Hash time lock contracts can help to eliminate the need for third parties in contracts
between two parties. Third parties that are often involved in contracts are lawyers,
banks, etc. Lawyers are often required to draw up contracts, and banks are often
required to help store money and then transfer it to the receiving party in the contract.

With hash time lock contracts, two parties could hypothetically set up contracts and
transfer money without the need for third parties. This is because the sending party
could create the conditional payment, and then the receiving party could agree to it,
receive it, and help validate the transaction in the process.

This could potentially revolutionize the way that many businesses interact with one another
and dramatically speed up the time that it takes for business deals to be set up.

## How do HTLC work?

The way that Hash Time Lock Contracts work is that the person who will be making the payment
sets up a specific hash, which represents the amount of money that will be paid. To receive
the payment, the recipient will have to create a cryptographic proof of payment, and he or
she will have to do this within the specified amount of time. The amount of time that the
recipient has to accept the payment can vary significantly from one Time Locked contract to
the next. If the recipient meets the deadline, then the money will be theirs, if he or she
fails to meet the deadline, it won’t. So, there is an often a lot at stake when it comes to
meeting deadlines from hash Time Locked contracts, when cryptocurrencies are being exchanged.

A Hash Time Lock Contract or HTLC is a class of payments that uses Hash Locked and Time Locked
to require that the receiver of a payment either acknowledge receiving the payment prior to a
deadline by generating cryptographic proof of payment or forfeit the ability to claim the payment,
returning(refunding) it to the payer.

Hash Time Lock Contracts (HTLCs) allow payments to be securely routed across multiple payment
channels which is super important because it is not optimal for a person to open a payment channel
with everyone he/she is transacting with.

- **Hash Locked** · A Hash Locked functions like “two-factor authentication” (2FA). It requires the intended recipient
to provide the correct secret passphrase to claim the funds.

- **Time Locked** · A Time Locked adds a “timeout” expiration date to a payment. It requires the intended recipient to
claim the funds prior to the expiry. Otherwise, the transaction defaults to enabling the original
sender of funds to claim a refund.

## Benefits of HTLCs
 
There are many benefits to these types of contracts. First, because they are time sensitive, it
prevents the person who is making the payment from having to wait indefinitely to find out whether
or not his or her payment goes through. Second, the person who makes the payment will not have to
waste his or her money if the payment is not accepted. It will simply be returned.

- **Time Sensitivity** · The time sensitive nature of the transaction prevents the sender from having
to wait forever to find out whether their payment went through. If the time runs out, the funds will
just be sent back to the sender, so they don’t have to worry and can wait for the process to unfold.

- **Trustless system** · As is the case with all smart contracts, trust is not needed as the rules are
already coded into the contract itself. Hash Time Lock Contracts take this one step further by
implementing a time limit for recipients to acknowledge the payment.

- **Validation of the Blockchain** · Transactions are validated because of the cryptographic proof of
payment required by the receiver.

- **Private Information's** · There are no complicated account setups or KYC/AML restrictions. Trade
directly from your wallet with a counterparty of your choice. Only the parties involved know the
details of the trade.

- **Trading across multiple Cryptocurrencies** · HTLC makes Cross-chain transactions easier and more
secure than ever. Cross chain transactions are the next step in the evolution of cryptocurrency
adoption. The easier it becomes to unite the hundreds of blockchain's that currently exist in
silos, the faster the technology as a whole can begin to scale and achieve mass adoption.

For more read the [documentation](https://swap.readthedocs.io).

| Hash Time Lock Contracts (HTLCs)       | Scripts                                                                                                           |
|:-------------------------------------- |:----------------------------------------------------------------------------------------------------------------: |
| Bitcoin: native BTC coin               | [htlc.script](https://github.com/movnetwork/swap/blob/master/swap/providers/bitcoin/contracts/htlc.script)        |
| Bytom v1.0: native BTM and more assets | [htlc.equity](https://github.com/movnetwork/swap/blob/master/swap/providers/bytom/contracts/htlc.equity)          |
| Ethereum: native ETH coin              | [htlc.sol](https://github.com/movnetwork/swap/blob/master/swap/providers/ethereum/contracts/htlc.sol)             |
| Ethereum for ERC20 tokens              | [htlc-erc20.sol](https://github.com/movnetwork/swap/blob/master/swap/providers/ethereum/contracts/htlc-erc20.sol) |
| Vapor: native BTM and more assets      | [htlc.equity](https://github.com/movnetwork/swap/blob/master/swap/providers/vapor/contracts/htlc.equity)          |
| XinFin: native XDC coin                | [htlc.sol](https://github.com/movnetwork/swap/blob/master/swap/providers/xinfin/contracts/htlc.sol)               |
| XinFin for XRC20 tokens                | [htlc-xrc20.sol](https://github.com/movnetwork/swap/blob/master/swap/providers/xinfin/contracts/htlc-xrc20.sol)   |

## Installation

PIP to install Swap globally, for Linux `sudo` may be required:

```
pip install swap
```

If you want to run the latest version of the code, you can install from git:

```
pip install git+git://github.com/meherett/swap.git
```

For the versions available, see the [tags on this repository](https://github.com/meherett/swap/tags).

## Development

We welcome pull requests. To get started, just fork this repo, clone it locally, and run:

```
pip install -e .[tests,docs] -r requirements.txt
```

## Testing

You can run the tests with:

```
pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Contributing

Feel free to open an [issue](https://github.com/meherett/swap/issues) if you find a problem, 
or a pull request if you've solved an issue. And also any help in testing, development, 
documentation and other tasks is highly appreciated and useful to the project. 
There are tasks for contributors of all experience levels.

For more information, see the [CONTRIBUTING.md](https://github.com/meherett/swap/blob/master/CONTRIBUTING.md) file.

## Donations

If You found this tool helpful consider making a donation:

| Coins                         | Addresses                                   |
| ----------------------------- | :-----------------------------------------: |
| Bitcoin `BTC`                 | 3GGNPvgbSpMHShcaZJGDXQn5wUJyTz7uoC          |
| Ethereum `ETH`, Tether `USDT` | 0x342798bbe9731a91e0557fa8ab0bce1eae6d6ae3  |
| Bytom `BTM`                   | bn1qumdsfgj06ae2nav2ws24t5jzmfagz2amj5arh3  |
| XinFin `XDC`                  | xdc95e80fc8ef98b92fe71514168c2e4b8f0ce38169 |

## License

Distributed under the [AGPL-3.0](https://github.com/meherett/swap/blob/master/LICENSE) license. 
See ``LICENSE`` for more information.
