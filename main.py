from colorama import Fore, Back, Style
import uploadNFT
import scrapNFT

menu = {}
menu['1']="Scrape NFT" 
menu['2']="Upload NFT with smart contract"
menu['3']="Verify smart contract"
menu['4']="Exit"

# Get string input from user
def getStringInput(msg):
    while True:
        userInput = input(msg)
        if len(userInput) > 0:
            break
        else:
            continue
    return userInput

# Get integer input from user
def getIntegerInput(msg):
    while True:
        try:
            userInput = input(msg)
        except ValueError:
            print("The input should be an integer. Please try again.")
            continue
        else:
            break
    return userInput


def main():
    while True: 
        options=menu.keys()
        for entry in options: 
            print(Fore.YELLOW + entry, Fore.YELLOW + menu[entry])
        selection=input(Fore.WHITE + "\nPlease Select: ") 
        
        # Scrap NFT
        if selection =='1': 
            print("\n1.1 Download NFT image and metadata into local storage")
            print("\nPlease enter the following details")
            scraping_environment = getIntegerInput("1. Environment of the collection that you wish to steal [1:testnets 2:mainnet]: ")
            if scraping_environment == "1":
                collection_to_steal_url = "https://testnets.opensea.io/collection/" + getStringInput("2. Collection name that you wish to steal (in lowercase): ")
            elif scraping_environment =="2":
                collection_to_steal_url = "https://opensea.io/collection/" + getStringInput("2. Collection name that you wish to steal (in lowercase): ")

            print("3. Scraping range of the token ID")
            scraping_range_start = getIntegerInput("Start: ")
            scraping_range_end = getIntegerInput("End: ")
            
            collection_name = getStringInput("4. New collection name: ")
            result = scrapNFT.steal_collection(collection_to_steal_url,collection_name,scraping_range_start,scraping_range_end)
            print("The NFT image and metadata are downloaded into ./collections/"+collection_name)
            
            print("\n1.2 Upload NFT image to IPFS")
            print("\nNow, open the browser and login to https://app.pinata.cloud/.")
            print("Upload the ./collections/"+collection_name+"/image folder to Pinata. There is no need to upload the json folder for now.")
            print("If the image folder is uploaded successfully, you will see the CID for it on the Pinata website (e.g. Qm....)")

            print("\n1.3 Replace the image path in json file with IPFS CID")
            CID_images = getStringInput("Please enter the CID of the IPFS image folder (e.g. Qm....): ")
            scrapNFT.replace_imagelink_json(collection_name, CID_images,result[0],result[1], result[2])
            print("Successfully replaced the image paths in json files.")

            print("\n1.4 Upload NFT json data to IPFS")
            print("\nNow, open the browser and login to https://app.pinata.cloud/.")
            print("Upload the ./collections/"+collection_name+"/json folder to Pinata.")
            print("If the json folder is uploaded successfully, you will see the CID for it on the Pinata website (e.g. Qm..../)")
            
            print("\nBy adding ipfs:// infront of CID, you will get the IPFS link for this json folder (e.g. ipfs://Qm..../). ")
            print("Please use this IPFS link (for json folder) as the IPFS link for the next step, which is uploading the NFT with smart contract.\n")
            
        # Upload NFT with smart contract
        elif selection == '2': 
            print("\nPlease enter the following details")
            uploadIPFS = getStringInput("1. IPFS link (e.g. ipfs://Qm..../): ")
            uploadMintNum = getIntegerInput("2. Number of NFT that you wish to mint (1 NFT = 0.01 ETH): ")
            contractName = getStringInput("3. Preferred smart contract name (e.g. NFT Contract): ")
            uploadNFT.deployContract(uploadIPFS,uploadMintNum,contractName)
        
        # Verify smart contract
        elif selection == '3':
            print("\nPlease enter the following details")
            verifyIPFS = getStringInput("1. IPFS link (e.g. ipfs://Qm..../): ")
            contractAddress = getStringInput("2. Smart contract address (e.g. 0x...): ")
            uploadNFT.verifyContract(contractAddress,verifyIPFS)
        
        # Exit
        elif selection == '4':
            print("\nEnd of program. Thanks for using it!")
            exit(0)
        else: 
            print("Unknown Option Selected!") 

if __name__ == '__main__':
    try:
        print("""
 .-----------------. .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| | ____  _____  | || |  _________   | || |  _________   | || |  ____  ____  | || |     _____    | || |  _________   | || |  _________   | |
| ||_   \|_   _| | || | |_   ___  |  | || | |  _   _  |  | || | |_   ||   _| | || |    |_   _|   | || | |_   ___  |  | || | |_   ___  |  | |
| |  |   \ | |   | || |   | |_  \_|  | || | |_/ | | \_|  | || |   | |__| |   | || |      | |     | || |   | |_  \_|  | || |   | |_  \_|  | |
| |  | |\ \| |   | || |   |  _|      | || |     | |      | || |   |  __  |   | || |      | |     | || |   |  _|  _   | || |   |  _|      | |
| | _| |_\   |_  | || |  _| |_       | || |    _| |_     | || |  _| |  | |_  | || |     _| |_    | || |  _| |___/ |  | || |  _| |_       | |
| ||_____|\____| | || | |_____|      | || |   |_____|    | || | |____||____| | || |    |_____|   | || | |_________|  | || | |_____|      | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
""")
        main()
    except KeyboardInterrupt:
        print("\nEnd of program. Thanks for using it!")
