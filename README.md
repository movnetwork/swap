# Swap

[![Build Status](https://travis-ci.org/meherett/swap.svg?branch=master)](https://travis-ci.org/meherett/swap?branch=master)
[![PyPI Version](https://img.shields.io/pypi/v/swap.svg?color=blue)](https://pypi.org/project/swap)
[![Documentation Status](https://readthedocs.org/projects/swap/badge/?version=latest)](https://swap.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/meherett/swap/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/meherett/swap?branch=master)

A python library for cross-chain atomic swap between the networks of two cryptocurrencies. 
Cross-chain atomic swap are the cheapest and most secure way to swap cryptocurrencies. 
It’s a brand new decentralized payment environment based on Hash Time Lock Contracts (HTLCs) protocol. 
[Documentation](https://swap.readthedocs.io)

## Available Cryptocurrencies

Swap has the following available [cryptocurrencies](https://github.com/meherett/swap/blob/master/cryptocurrencies) to swap:

| Cryptocurrencies                                        | Mainnet | Testnet | Solonet | 
| ------------------------------------------------------- | :-----: | :-----: | :-----: |
| [Bitcoin](https://github.com/bitcoin/bitcoin) `BTC`     | Yes     | Yes     | None    |
| [Bytom](https://github.com/bytom/bytom) `BTM`, `Assets` | Yes     | No      | No      |

## Benefits of HTLC's
 
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

## Installation

PIP to install **swap** globally. For Linux `sudo` may be required.

```
$ pip install swap
```

For the versions available, see the [tags on this repository](https://github.com/meherett/swap/tags).

## Development

We welcome pull requests. Just fork this repo, clone it locally, and run:

```
$ pip install -e .[tests,docs] -r requirements.txt
```

## Testing

Tests are still under development.

You can run the tests with:

```
$ pytest
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Contributing

Feel free to open an issue if you find a problem, or a pull request if you've solved an issue.

## License

Distributed under the [AGPL-3.0](https://github.com/meherett/swap/blob/master/LICENSE) license. 
See ``LICENSE`` for more information.
