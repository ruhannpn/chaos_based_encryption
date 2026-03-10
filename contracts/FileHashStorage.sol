// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileHashStorage {

    mapping(string => bytes32) private fileHashes;

    event HashStored(string fileId, bytes32 hash);

    function storeHash(string memory fileId, bytes32 hash) public {
        fileHashes[fileId] = hash;
        emit HashStored(fileId, hash);
    }

    function verifyHash(string memory fileId, bytes32 hash) public view returns (bool) {
        return fileHashes[fileId] == hash;
    }

    function getHash(string memory fileId) public view returns (bytes32) {
        return fileHashes[fileId];
    }
}
