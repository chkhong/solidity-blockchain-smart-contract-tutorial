// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    
  // this gets initialized to 0
  uint256 favouriteNumber;
  
  struct People {
    uint256 favouriteNumber;
    string name;
  }
  
  People[] public people;
  mapping(string => uint256) public nameToFavouriteNumber;
  
  // public, private, internal, external
  function store(uint256 _favouriteNumber) public {
    favouriteNumber = _favouriteNumber;
  }
  
  //view -> view variables in contract, pure -> does simple calculation without changing variables
  function retrieve() public view returns(uint256) {
    return favouriteNumber;
  }
  
  //memory -> string variable destroyed after function terminates, storage -> string variable does not destroy after function terminates
  function addPerson(string memory _name, uint256 _favouriteNumber) public {
    people.push(People(_favouriteNumber, _name));
    nameToFavouriteNumber[_name] = _favouriteNumber;
  }
}