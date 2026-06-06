// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LicenseCheck {
    // Mapping to store which blockchain addresses own a valid license
    mapping(address => bool) public hasLicense;

    // Function to grant a license (Simulating a purchase)
    function grantLicense(address _user) public {
        hasLicense[_user] = true;
    }

    // Function to check if a user is authorized
    function verifyLicense(address _user) public view returns (bool) {
        return hasLicense[_user];
    }
}