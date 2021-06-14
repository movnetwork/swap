#!/usr/bin/env python3

from binascii import unhexlify, hexlify
from solcx import compile_standard

import json

from ..config import ethereum
from .wallet import Wallet
from .rpc import get_web3
from .utils import is_address, to_checksum_address
from ...utils.exceptions import AddressError, BalanceError, BuildTransactionError

# Ethereum configuration
ethereum = ethereum()


HTLC_SCRIPT = """
pragma solidity >=0.5.0 <0.6.0;


contract HTLC {

    event LogHTLCNew(
        bytes32 indexed contractId,
        address indexed sender,
        address indexed receiver,
        uint amount,
        bytes32 hashlock,
        uint timelock
    );
    event LogHTLCWithdraw(bytes32 indexed contractId);
    event LogHTLCRefund(bytes32 indexed contractId);

    struct LockContract {
        address payable sender;
        address payable receiver;
        uint amount;
        bytes32 hashlock; // sha-2 sha256 hash
        uint timelock; // UNIX timestamp seconds - locked UNTIL this time
        bool withdrawn;
        bool refunded;
        bytes32 preimage;
    }

    modifier fundsSent() {
        require(msg.value > 0, "msg.value must be > 0");
        _;
    }
    modifier futureTimelock(uint _time) {
        // only requirement is the timelock time is after the last blocktime (now).
        // probably want something a bit further in the future then this.
        // but this is still a useful sanity check:
        require(_time > now, "timelock time must be in the future");
        _;
    }
    modifier contractExists(bytes32 _contractId) {
        require(haveContract(_contractId), "contractId does not exist");
        _;
    }
    modifier hashlockMatches(bytes32 _contractId, bytes32 _x) {
        require(
            contracts[_contractId].hashlock == sha256(abi.encodePacked(_x)),
            "hashlock hash does not match"
        );
        _;
    }
    modifier withdrawable(bytes32 _contractId) {
        require(contracts[_contractId].receiver == msg.sender, "withdrawable: not receiver");
        require(contracts[_contractId].withdrawn == false, "withdrawable: already withdrawn");
        require(contracts[_contractId].timelock > now, "withdrawable: timelock time must be in the future");
        _;
    }
    modifier refundable(bytes32 _contractId) {
        require(contracts[_contractId].sender == msg.sender, "refundable: not sender");
        require(contracts[_contractId].refunded == false, "refundable: already refunded");
        require(contracts[_contractId].withdrawn == false, "refundable: already withdrawn");
        require(contracts[_contractId].timelock <= now, "refundable: timelock not yet passed");
        _;
    }

    mapping (bytes32 => LockContract) contracts;

    /**
     * @dev Sender sets up a new hash time lock contract depositing the ETH and
     * providing the reciever lock terms.
     *
     * @param _receiver Receiver of the ETH.
     * @param _hashlock A sha-2 sha256 hash hashlock.
     * @param _timelock UNIX epoch seconds time that the lock expires at.
     *                  Refunds can be made after this time.
     * @return contractId Id of the new HTLC. This is needed for subsequent
     *                    calls.
     */
    function newContract(address payable _receiver, bytes32 _hashlock, uint _timelock)
        external
        payable
        fundsSent
        futureTimelock(_timelock)
        returns (bytes32 contractId)
    {
        contractId = sha256(
            abi.encodePacked(
                msg.sender,
                _receiver,
                msg.value,
                _hashlock,
                _timelock
            )
        );

        // Reject if a contract already exists with the same parameters. The
        // sender must change one of these parameters to create a new distinct
        // contract.
        if (haveContract(contractId))
            revert("Contract already exists");

        contracts[contractId] = LockContract(
            msg.sender,
            _receiver,
            msg.value,
            _hashlock,
            _timelock,
            false,
            false,
            0x0
        );

        emit LogHTLCNew(
            contractId,
            msg.sender,
            _receiver,
            msg.value,
            _hashlock,
            _timelock
        );
    }

    /**
     * @dev Called by the receiver once they know the preimage of the hashlock.
     * This will transfer the locked funds to their address.
     *
     * @param _contractId Id of the HTLC.
     * @param _preimage sha256(_preimage) should equal the contract hashlock.
     * @return bool true on success
     */
    function withdraw(bytes32 _contractId, bytes32 _preimage)
        external
        contractExists(_contractId)
        hashlockMatches(_contractId, _preimage)
        withdrawable(_contractId)
        returns (bool)
    {
        LockContract storage c = contracts[_contractId];
        c.preimage = _preimage;
        c.withdrawn = true;
        c.receiver.transfer(c.amount);
        emit LogHTLCWithdraw(_contractId);
        return true;
    }

    /**
     * @dev Called by the sender if there was no withdraw AND the time lock has
     * expired. This will refund the contract amount.
     *
     * @param _contractId Id of HTLC to refund from.
     * @return bool true on success
     */
    function refund(bytes32 _contractId)
        external
        contractExists(_contractId)
        refundable(_contractId)
        returns (bool)
    {
        LockContract storage c = contracts[_contractId];
        c.refunded = true;
        c.sender.transfer(c.amount);
        emit LogHTLCRefund(_contractId);
        return true;
    }

    /**
     * @dev Get contract details.
     * @param _contractId HTLC contract id
     * @return All parameters in struct LockContract for _contractId HTLC
     */
    function getContract(bytes32 _contractId)
        public
        view
        returns (
            address sender,
            address receiver,
            uint amount,
            bytes32 hashlock,
            uint timelock,
            bool withdrawn,
            bool refunded,
            bytes32 preimage
        )
    {
        if (haveContract(_contractId) == false)
            return (address(0), address(0), 0, 0, 0, false, false, 0);
        LockContract storage c = contracts[_contractId];
        return (
            c.sender,
            c.receiver,
            c.amount,
            c.hashlock,
            c.timelock,
            c.withdrawn,
            c.refunded,
            c.preimage
        );
    }

    /**
     * @dev Is there a contract with id _contractId.
     * @param _contractId Id into contracts mapping.
     */
    function haveContract(bytes32 _contractId)
        internal
        view
        returns (bool exists)
    {
        exists = (contracts[_contractId].sender != address(0));
    }

}
"""

# Solidity source code
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "HTLC.sol": {
            "content": HTLC_SCRIPT
        }
    },
    "settings":
        {
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode"
                        , "evm.bytecode.sourceMap"
                    ]
                }
            }
        }
})


class HTLC:

    # Initialization
    def __init__(self, network="ropsten"):

        # HTLC info's
        self.contract_init = None
        # Initializing web3 and getting previous hash & contract address of htlc
        self._hash, _, self.web3 = get_web3(network=network)
        # get bytecode
        self._bytecode = compiled_sol["contracts"]["HTLC.sol"]["HTLC"]["evm"]["bytecode"]["object"]
        # get abi
        self._abi = json.loads(compiled_sol["contracts"]["HTLC.sol"]["HTLC"]["metadata"])["output"]["abi"]
        # get abi
        self._opcode = compiled_sol["contracts"]["HTLC.sol"]["HTLC"]["evm"]["bytecode"]["opcodes"]

    # Build transaction for HTLC
    def build_transaction(self, wallet=None, amount=0):

        # Checking waller instance
        if wallet and not isinstance(wallet, Wallet):
            raise ValueError("invalid wallet instance, only takes Wallet class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")
        # Setting wallet
        if wallet:
            account = self.web3.eth.account.privateKeyToAccount(wallet.private_key())
            new_htlc = self.web3.eth.contract(abi=self._abi, bytecode=self._bytecode)
            # Submit the transaction that deploys the contract
            construct_txn = new_htlc.constructor().buildTransaction({
                "from": account.address,
                "value": amount,
                "nonce": self.web3.eth.getTransactionCount(account.address),
                "gas": ethereum["gas"],
                "gasPrice": self.web3.eth.gasPrice
            })
            signed = account.signTransaction(construct_txn)
            try:
                self._hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
            except ValueError as value_error:
                if str(value_error).find("sender doesn't have enough funds to send tx") != -1:
                    raise BalanceError("insufficient spend balance")
                raise value_error
        else:
            self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
            new_htlc = self.web3.eth.contract(abi=self._abi, bytecode=self._bytecode)
            # Submit the transaction that deploys the contract
            self._hash = new_htlc.constructor().transact()
        return self

    def hash(self):
        return hexlify(self._hash).decode()

    def contract_address(self):
        tx_receipt = self.web3.eth.getTransactionReceipt(transaction_hash=self._hash)
        if tx_receipt is None:
            raise BuildTransactionError("HTLC %s still not mined, wait for it to be mined..." % self.hash())
        return to_checksum_address(tx_receipt.contractAddress)

    def init(self, secret_hash, recipient_address, sender_address, end_time):

        # Checking parameters
        if not isinstance(secret_hash, str):
            raise TypeError("secret hash must be string format")
        if len(secret_hash) != 64:
            raise ValueError("invalid secret hash, length must be 64.")
        if not isinstance(recipient_address, str):
            raise TypeError("recipient address must be string format")
        if not is_address(recipient_address):
            raise AddressError("invalid ethereum recipient %s address" % recipient_address)
        if not isinstance(sender_address, str):
            raise TypeError("sender address must be string format")
        if not is_address(sender_address):
            raise AddressError("invalid ethereum sender %s address" % sender_address)
        if not isinstance(end_time, int):
            raise TypeError("end_time must be integer format")

        self.contract_init = (
            to_checksum_address(recipient_address),
            unhexlify(secret_hash),
            int(end_time),
            to_checksum_address(sender_address)
        )
        return self

    def bytecode(self):
        return self._bytecode

    def opcode(self):
        return self._opcode

    def abi(self):
        return self._abi
