import string
import subprocess
import os

# Read all content from the .env file and store into an array
def retrieveFile(filename):
    lines = []
    with open(filename,"r") as f:
        lines = f.readlines()
    f.close()
    return lines


# Rewrite file content with the updated array
def rewriteFile(filename, filearray):
    with open(filename, "w") as f:
        filearray = "".join(filearray)
        f.write(filearray)
    f.close()


# Deploy contract and mint NFTs
def deployContract(ipfs,mintNum,contractName):

    # Change the IPFS and MINT_NUM values in the .env file
    envFile = os.getcwd()+"/uploadNFT/.env"
    envContent = retrieveFile(envFile)
    for i,line in enumerate(envContent):
        if line.startswith("IPFS="):
            newline="IPFS=\"" + ipfs + "\"\n"
            envContent[i] = newline          # Replace current line with new line
            #envContent.insert(i,newline)
        if line.startswith("MINT_NUM="):
            newline="MINT_NUM=" + str(mintNum) + "\n"
            envContent[i] = newline          # Replace current line with new line
    rewriteFile(envFile,envContent)
    
    # Change the contract name in the ERC721Contract.sol
    contractFile = os.getcwd()+"/uploadNFT/contracts/ERC721Contract.sol"
    contractContent = retrieveFile(contractFile)
    for i,line in enumerate(contractContent):
        if line.startswith("\tstring public contractName = "):
            newline="\tstring public contractName = \"" + contractName + "\";\n"
            contractContent[i] = newline      # Replace current line with new line
    rewriteFile(contractFile,contractContent)

    # Run uploadNFT/main.js to upload contract
    print("\nUploading smart contract and minting NFTs now, it will take awhile ...\n")
    subprocess.call(["npx", "hardhat", "run", "main.js", "--network", "rinkeby"], cwd=os.getcwd()+"/uploadNFT")


# Verify whether contract is deployed successfully
def verifyContract(contractAddress,verifyIPFS):
    print("\nThe verification process might be failed if the contract is not fully deployed. You may verify it over and over again until you see a message indicates that it is verified!\n")
    while True:
        subprocess.call(['npx', 'hardhat', 'verify', '--network', 'rinkeby', contractAddress, verifyIPFS], cwd=os.getcwd()+"/uploadNFT")
        userInput = input("\nWant to verify the same contract and IPFS again? (Y/n): ")
        if userInput == "Y":
            print("")   # For output formatting
            continue
        else:
            print("")   # For output formatting
            break

