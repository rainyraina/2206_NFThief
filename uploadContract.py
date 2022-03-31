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

# Get the contract name from user input
def getContractName():
    while True:
        contractName = input("Please enter a preferred smart contract name (e.g. NFT Contract): ")
        if len(contractName) > 0:
            break
        else:
            continue
    return contractName

# Upload contract and mint NFTs
def uploadContract(ipfs,mintNum,contractName):

    # Change the IPFS and MINT_NUM values in the .env file
    envFile = os.getcwd()+"/uploadContract/.env"
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
    contractFile = os.getcwd()+"/uploadContract/contracts/ERC721Contract.sol"
    contractContent = retrieveFile(contractFile)
    for i,line in enumerate(contractContent):
        if line.startswith("\tstring public contractName = "):
            newline="\tstring public contractName = \"" + contractName + "\";\n"
            contractContent[i] = newline      # Replace current line with new line
    rewriteFile(contractFile,contractContent)

    # Run main.js to upload contract
    print("\nUploading smart contract and minting NFTs now, it will take awhile ...\n")
    output = subprocess.check_output(["npx", "hardhat", "run", "main.js", "--network", "rinkeby"], cwd=os.getcwd()+"/uploadContract")
    print(output.decode("utf-8"))
    # From the command output, get the smart contract address
    outputList = output.decode("utf-8").split("\n")
    contractAddress = ""
    for i in outputList:
        if i.startswith("Smart contract address: "):
            contractAddress = i[24:]
    
    # Verify contract if contract address exists
    print("\nVerifying smart contract now ...\n")
    if len(contractAddress)>0:
        subprocess.call(['npx', 'hardhat', 'verify', '--network', 'rinkeby', contractAddress, ipfs], cwd=os.getcwd()+"/uploadContract")
    else:
        print("There is no smart contract address to verify. Please ensure the contract is uploaded in the previous step.\n")
    
ipfs = "ipfs://QmYjhUCiQrYZCZNRk2wNbfuNgJF6Aan1dmnydPYjyS6DQ1/"
mintNum = 2
contractName = getContractName()

uploadContract(ipfs,mintNum,contractName)

