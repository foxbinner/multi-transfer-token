<div align="center">

# Transfer Any Token

[![Python][python-version-img]][python-version-url]
[![Web3][web3-version-img]][web3-version-url]
[![Issues][repo_issues_img]][repo_issues_url]
[![License][repo_license_img]][repo_license_url]

Easily transfer any tokens (e.g., Sepolia USDC) from <br>**single address to multiple addresses** or consolidate funds from <br>**multiple addresses into one**—all in an instant!

<p align="center">
  <img width="45%" alt="Main to Multi" src="https://i.postimg.cc/MTKYYBjb/main-to-multi-token.png">
  <img width="45%" alt="Multi to Main" src="https://i.postimg.cc/nL1k72Mh/multi-to-main-token.png">
</p>

</div>

## 🚀 Introduction

Transferring any tokens (e.g., Sepolia USDC, Base USDC) to multiple addresses can be time-consuming when done manually with wallets (e.g., Metamask,  Rabby). My solution simplifies this with two Python scripts:

- **Single-to-Multiple Transfers** – Send any tokens from one address to multiple recipients in a single transaction.
- **Multiple-to-Single Transfers** – Consolidate tokens from multiple addresses into a single destination efficiently.

Save time, reduce complexity, and make token transfers easier! 🧙‍♂️

## 📖 User Manual

- Keep your addresses and private keys formatted and saved in ```mainwallet.txt``` and ```recipients.txt```.
- Change the following values to start with:
```
AMOUNT = 0.1
RPC_URL = 'https://ethereum-sepolia-rpc.publicnode.com'
CHAIN_ID = 11155111
TOKEN_CONTRACT = '0xadbf21cCdFfe308a8d83AC933EF5D3c98830397F'
TICKER = 'USDC'
EXPLORER = 'https://sepolia.etherscan.io'
GAS_LIMIT = 60000
```

## 🚩 Contribution

Found an issue or have a suggestion? Report it in [issues][repo_issues_url] or fork & submit a pull request.<br>Every contribution counts! 🎉

## 📄 License

This project is open-source and licensed under the [MIT license][repo_license_url].

<!-- Repo Links -->
[repo_url]: https://github.com/foxbinner/multi-transfer-token
[repo_license_url]: https://github.com/foxbinner/multi-transfer-token/blob/main/LICENSE
[repo_issues_url]: https://github.com/foxbinner/multi-transfer-token/issues

[repo_license_img]: https://img.shields.io/badge/license-MIT-red
[repo_issues_img]: https://img.shields.io/badge/feedback-open-green

<!-- Extras -->
[web3-version-img]: https://img.shields.io/badge/web3-7.7.0-blue
[web3-version-url]: https://pypi.org/project/web3/7.7.0
[python-version-img]: https://img.shields.io/badge/python-3.12.9-blue
[python-version-url]: https://www.python.org/downloads
