// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract OrbitalDataMarketplace {
    struct DataListing {
        address seller;
        string dataDescription;
        uint256 price;
        bool isSold;
        uint256 timestamp; // Timestamp of the listing
    }

    mapping(uint256 => DataListing) public listings;
    uint256 public listingCount;

    event DataListed(uint256 indexed listingId, address indexed seller, string dataDescription, uint256 price, uint256 timestamp);
    event DataSold(uint256 indexed listingId, address indexed buyer, uint256 price, uint256 timestamp);
    event DataUpdated(uint256 indexed listingId, string newDataDescription, uint256 newPrice);
    event DataRemoved(uint256 indexed listingId, address indexed seller);

    modifier onlySeller(uint256 _listingId) {
        require(msg.sender == listings[_listingId].seller, "Only the seller can perform this action");
        _;
    }

    modifier validPrice(uint256 _price) {
        require(_price > 0, "Price must be greater than zero");
        _;
    }

    // Function to list data for sale
    function listData(string memory _dataDescription, uint256 _price) public validPrice(_price) {
        listingCount++;
        listings[listingCount] = DataListing(msg.sender, _dataDescription, _price, false, block.timestamp);
        emit DataListed(listingCount, msg.sender, _dataDescription, _price, block.timestamp);
    }

    // Function to buy data
    function buyData(uint256 _listingId) public payable {
        DataListing storage listing = listings[_listingId];
        require(msg.value == listing.price, "Incorrect price");
        require(!listing.isSold, "Data already sold");

        listing.isSold = true;
        payable(listing.seller).transfer(msg.value);
        emit DataSold(_listingId, msg.sender, listing.price, block.timestamp);
    }

    // Function to update data listing
    function updateDataListing(uint256 _listingId, string memory _newDataDescription, uint256 _newPrice) public onlySeller(_listingId) validPrice(_newPrice) {
        DataListing storage listing = listings[_listingId];
        listing.dataDescription = _newDataDescription;
        listing.price = _newPrice;
        emit DataUpdated(_listingId, _newDataDescription, _newPrice);
    }

    // Function to remove a data listing
    function removeDataListing(uint256 _listingId) public onlySeller(_listingId) {
        require(!listings[_listingId].isSold, "Cannot remove sold data");
        delete listings[_listingId];
        emit DataRemoved(_listingId, msg.sender);
    }

    // Function to get data listing details
    function getDataListing(uint256 _listingId) public view returns (address, string memory, uint256, bool, uint256) {
        DataListing memory listing = listings[_listingId];
        return (listing.seller, listing.dataDescription, listing.price, listing.isSold, listing.timestamp);
    }

    // Function to withdraw funds in case of contract issues
    function withdrawFunds() public {
        require(msg.sender == address(this), "Only the contract can withdraw funds");
        payable(msg.sender).transfer(address(this).balance);
    }

    // Fallback function to accept Ether
    receive() external payable {}

    // Function to get the total number of listings
    function totalListings() public view returns (uint256) {
        return listingCount;
    }
}
