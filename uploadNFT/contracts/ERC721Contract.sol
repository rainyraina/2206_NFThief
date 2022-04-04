pragma solidity ^0.8.0;
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";

contract ERC721Contract is ERC721Enumerable, Ownable {
	using SafeMath for uint256;		// For the .mul function
	using Counters for Counters.Counter;	// For incrementing token ID

	Counters.Counter private tokenID;
	uint public constant PRICE = 0.01 ether;	// ETH spent for minting 1 NFT (0.01 is the minimum amount required)
	string public baseTokenURI;
	string public contractName = "Contract 9.2";
	
	// set the contract name with baseTokenURI
	constructor(string memory baseURI) ERC721(contractName, "NFTC") {
		setBaseURI(baseURI);
	}
	function _baseURI() internal view virtual override returns (string memory) {
		return baseTokenURI;
	}
	function setBaseURI(string memory _baseTokenURI) public onlyOwner {
		baseTokenURI = _baseTokenURI;
	}

	// Mint all NFTs
	function mintAllNFTs(uint NFTcount) public payable {
		require(NFTcount > 0, "There is no NFT to mint");	// Check if there is NFT to mint
		require(msg.value >= PRICE.mul(NFTcount), "There is no enough ETH in your wallet to mint the NFT(s).");	// Check if there is enough ETH

		// Loop through to mint each NFT, with token ID incremented by 1 (initial token ID = 0)
		for (uint i = 0; i < NFTcount; i++) {
			_safeMint(msg.sender, tokenID.current());
			tokenID.increment();
		}
	}
}
