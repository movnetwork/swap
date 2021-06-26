pragma solidity ^0.8.3;

/**
 * XinFin smart contract -> Solidity language
 *
 * @title Hash Time Lock Contract (HTLC)
 *
 * @author Meheret Tesfaye Batu <meherett@zoho.com>
 *
 * A Hash Time Lock Contract is essentially a type of payment in which two
 * people agree to a financial arrangement where one party will pay the other
 * party a certain amount of cryptocurrency, such as Bitcoin or Ethereum assets.
 * However, because these contracts are Time Locked, the receiving party only
 * has a certain amount of time to accept the payment, otherwise the money
 * can be returned to the sender.
 */
contract HTLC {

    struct LockedContract {
        bytes32 secret_hash;
        address payable recipient;
        address payable sender;
        uint endtime;
        uint amount;
        bool withdrawn;
        bool refunded;
        string preimage;
    }

    mapping (bytes32 => LockedContract) locked_contracts;

    event log_fund (
        bytes32 indexed locked_contract_id,
        bytes32 secret_hash,
        address indexed recipient,
        address indexed sender,
        uint endtime,
        uint amount
    );
    event log_withdraw (
        bytes32 indexed locked_contract_id
    );
    event log_refund (
        bytes32 indexed locked_contract_id
    );

    modifier fund_sent () {
        require(msg.value > 0, "msg.value must be > 0");
        _;
    }
    modifier future_endtime (uint _endtime) {
        require(_endtime > block.timestamp, "endtime time must be in the future");
        _;
    }
    modifier is_locked_contract_exist (bytes32 _locked_contract_id) {
        require(have_locked_contract(_locked_contract_id), "locked_contract_id does not exist");
        _;
    }
    modifier check_secret_hash_matches (bytes32 _locked_contract_id, string memory _preimage) {
        require(locked_contracts[_locked_contract_id].secret_hash == sha256(abi.encodePacked(_preimage)), "secret_hash hash does not match");
        _;
    }
    modifier withdrawable (bytes32 _locked_contract_id) {
        require(locked_contracts[_locked_contract_id].recipient == msg.sender, "withdrawable: not recipient");
        require(locked_contracts[_locked_contract_id].withdrawn == false, "withdrawable: already withdrawn");
        _;
    }
    modifier refundable (bytes32 _locked_contract_id) {
        require(locked_contracts[_locked_contract_id].sender == msg.sender, "refundable: not sender");
        require(locked_contracts[_locked_contract_id].refunded == false, "refundable: already refunded");
        require(locked_contracts[_locked_contract_id].withdrawn == false, "refundable: already withdrawn");
        require(locked_contracts[_locked_contract_id].endtime <= block.timestamp, "refundable: endtime not yet passed");
        _;
    }

    /**
     * @dev Sender sets up a new hash time lock contract depositing the ETH.
     *
     * @param _secret_hash: A sha-2 sha256 hash.
     * @param _recipient: Receiver of the ETH.
     * @param _sender: Sender of the ETH.
     * @param _endtime: UNIX epoch seconds time that the lock expires at.
     *
     * return locked_contract_id of the new HTLC. This is needed for subsequent calls.
     */
    function fund (bytes32 _secret_hash, address payable _recipient, address payable _sender, uint _endtime) external payable fund_sent future_endtime (_endtime) returns (bytes32 locked_contract_id) {

        require(msg.sender == _sender, "msg.sender must be same with sender address");

        locked_contract_id = sha256(abi.encodePacked(
            _secret_hash, _recipient, msg.sender, _endtime, msg.value
        ));

        if (have_locked_contract(locked_contract_id))
            revert("this locked contract already exists");

        locked_contracts[locked_contract_id] = LockedContract(
            _secret_hash, _recipient, _sender, _endtime, msg.value, false, false, ""
        );

        emit log_fund (
            locked_contract_id, _secret_hash, _recipient, msg.sender, _endtime, msg.value
        );
    }

    /**
     * @dev Called by the recipient once they know the preimage of the secret_hash.
     *
     * @param _locked_contract_id:  Id of the HTLC.
     * @param _preimage: sha256(_preimage) should equal the contract secret_hash.
     *
     * @return bool true on success
     */
    function withdraw (bytes32 _locked_contract_id, string memory _preimage) external is_locked_contract_exist (_locked_contract_id) check_secret_hash_matches (_locked_contract_id, _preimage) withdrawable(_locked_contract_id) returns (bool) {

        LockedContract storage locked_contract = locked_contracts[_locked_contract_id];

        locked_contract.preimage = _preimage;
        locked_contract.withdrawn = true;
        locked_contract.recipient.transfer(
            locked_contract.amount
        );

        emit log_withdraw (_locked_contract_id);
        return true;
    }

    /**
     * @dev Called by the sender if there was no withdraw AND the time lock has expired.
     *
     * @param _locked_contract_id: Id of HTLC to refund from.
     *
     * @return bool true on success
     */
    function refund (bytes32 _locked_contract_id) external is_locked_contract_exist (_locked_contract_id) refundable (_locked_contract_id) returns (bool) {

        LockedContract storage locked_contract = locked_contracts[_locked_contract_id];

        locked_contract.refunded = true;
        locked_contract.sender.transfer(
            locked_contract.amount
        );

        emit log_refund (_locked_contract_id);
        return true;
    }

    /**
     * @dev Get contract details.
     *
     * @param _locked_contract_id: HTLC contract id
     *
     * return tuple parameters in struct LockContract for _locked_contract_id HTLC
     */
    function get_locked_contract (bytes32 _locked_contract_id) public view returns (
        bytes32 id, bytes32 secret_hash, address recipient, address sender, uint endtime, uint amount, bool withdrawn, bool refunded, string memory preimage
    ) {
        if (have_locked_contract(_locked_contract_id) == false)
            return (0, 0, address(0), address(0), 0, 0, false, false, "");

        LockedContract storage locked_contract = locked_contracts[_locked_contract_id];

        return (
            _locked_contract_id,
            locked_contract.secret_hash,
            locked_contract.recipient,
            locked_contract.sender,
            locked_contract.endtime,
            locked_contract.amount,
            locked_contract.withdrawn,
            locked_contract.refunded,
            locked_contract.preimage
        );
    }

    /**
     * @dev Is there a contract with id _locked_contract_id.
     *
     * @param _locked_contract_id Id into contracts mapping.
     */
    function have_locked_contract (bytes32 _locked_contract_id) internal view returns (bool exists) {
        exists = (locked_contracts[_locked_contract_id].sender != address(0));
    }
}