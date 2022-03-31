const { utils } = require("ethers");

const { IPFS, MINT_NUM } = process.env;

async function main() {

    // Get the wallet address
    const [owner] = await hre.ethers.getSigners();
    
    // Get the IPFS link from .env
    const baseTokenURI = IPFS;
    console.log("IPFS to be uploaded:", baseTokenURI);

    // Get the ERC721Contract and deploy it
    const smartContractFactory = await hre.ethers.getContractFactory("ERC721Contract");
    const smartContract = await smartContractFactory.deploy(baseTokenURI);
    await smartContract.deployed();
    console.log("Smart contract address:", smartContract.address);   
    
    // Mint NFTs based on the MINT_NUM defined in .env
    eth = MINT_NUM;
    eth = eth * 0.01;
    console.log("Number of NFT(s):",MINT_NUM)
    console.log("ETH required to mint NFT(s):",eth)
    txn = await smartContract.mintAllNFTs(MINT_NUM, { value: utils.parseEther(eth.toString())});
    await txn.wait()
    console.log("Successfully minted!");
}

main()   
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
