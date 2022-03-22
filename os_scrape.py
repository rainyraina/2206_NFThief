from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO
import re
import os
import io
import pandas as pd
import numpy as np


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

#Get the collection name to steal from
collection_to_steal = "https://opensea.io/collection/" + input("Enter Collection name in lower case: ")
collection_name = input("Enter new collection name: ")

#Stolen nft stored under images folder
target_path ='./images'

#Function to save NFT as files
def write_text(data: bytes, path: str):
    with open(path, 'wb') as file:
        file.write(data)

#Function to get the api url that displays the json data
def get_api_url(contract_add, token_id):
	links = []

	#Construct the asset url of the indivual nft
	asset_url = "https://opensea.io/assets/" + contract_add + "/" + token_id
	#print("asset url:" + asset_url)

	#Scrape the asset url to get the api url
	req = Request(asset_url, headers={'User-Agent': 'Mozilla/5.0'})
	html_page = urlopen(req)
	soup = BeautifulSoup(html_page, "lxml")

	#Scraping all the urls in the page
	for link in soup.findAll('a'):
	    links.append(link.get('href'))


	#Looking for this substring
	substring = "https://opensea.mypinata.cloud/ipfs/"

	#Getting the unique key of the collection
	for link in links:
		if link != None and substring in link:
			api_url = re.search("https://opensea.mypinata.cloud/ipfs/(.*)/", link)
			print(api_url)	
			print(link)

			return(api_url.group(0))



def steal_collection(collection_url: str):


	#Declaring the arrays
	links = []
	stolen_tokens = []
	api_list = []
	json_list = []
	image_list = []
	name_list = []
	description_list = []
	external_url_list = []
	attributes_list = []
	token_list = []

	#Scraping the web for assets url
	req = Request(collection_url, headers={'User-Agent': 'Mozilla/5.0'})
	html_page = urlopen(req)
	soup = BeautifulSoup(html_page, "lxml")

	for link in soup.findAll('a'):
	    links.append(link.get('href'))


	for link in links:
		if link!= None:
			if link.startswith("/assets"):
				contract_address = re.search('/assets/(.*)/', link)
				token_id = link[-4:]
				if "/" not in token_id:
					if token_id.isalpha()== False:
						if not token_id.startswith("0"):
							stolen_tokens.append(token_id)
					else:
						print(token_id)

	#Using the scrapped token id to get the api url
	stolen_tokens = list(dict.fromkeys(stolen_tokens))


	#before appending token id at the back
	#token standard: ERC-721
	#Have to find the api url automatically
	#get the api url using contract address and token id

	contract_address = contract_address.group(1)
	
	for token in stolen_tokens:

		#Invoke the get_api_url function
		#not all assets pages contain the link so must loop through
		api_url = get_api_url(contract_address, token)

		if api_url!= None:
			break
		else:
			continue

	#Specify the range of NFTs
	i = 0
	while i < 100:
		unique_api_url = api_url + str(i)
		api_list.append(unique_api_url)
		i+=1
		print(unique_api_url)

	#get all json data
	for api in api_list:
		r = requests.get(api)
		json_list.append(r)


	for json in json_list:
		#Convert json data to string
		json = str(json.json())


		#Extract data from the json
		try:
			found_token = re.search("'id': (.+?), ", json).group(1)
			found_image = re.search("'image': '(.+?)', ", json).group(1)
			found_name = json.split("'name': \'")[1].split(". \",")[0]
			found_name = re.search("'name': '(.+?)', ", json).group(1)
			found_description = json.split("'description': ")[1].split(", 'e")[0]
			found_external_url = re.search("'external_url': '(.+?)',", json).group(1)
			found_attributes = json.split("'attributes': ")[1].split("}]}")[0]

		except AttributeError:
			pass

		#Append extracted json data to array
		token_list.append(found_token)
		image_list.append(found_image)
		name_list.append(found_name)
		description_list.append(found_description)
		external_url_list.append(found_external_url)
		attributes_list.append(found_attributes)


	# For Testing purposes
	# print("IMAGE LIST")
	# print(len(image_list))
	# print(image_list)

	# print("\nNAME LIST")
	# print(len(name_list))
	# print(name_list)

	# print("\nDESCRIPTION LIST")
	# print(len(description_list))
	# print(description_list)

	# print("\nURL LIST")
	# print(len(external_url_list))
	# print(external_url_list)

	#Create folder to store NFTs
	target_folder = os.path.join(target_path,'_'.join(collection_name.lower().split(' ')))
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)

	#call the download function
	download_count=0
	for url in image_list:
	    svg = requests.get(url).content
	    filename = './images/'+ collection_name + '/' +url[-68:]
	    write_text(svg, filename)
	    download_count+=1
	    print(download_count)
	    print(filename)


	#For Testing purposes:
	# print(len(token_list))
	# print(len(image_list))
	# print(len(name_list))
	# print(len(description_list))
	# print(len(external_url_list))
	# print(len(attributes_list))

	#Write to csv file
	token_id_col = np.array(token_list)
	image_col = np.array(image_list)
	name_col = np.array(name_list)
	desc_col = np.array(description_list)
	url_col = np.array(external_url_list)
	attributes_col = np.array(attributes_list)

	#Generate CSV
	df = pd.DataFrame({"Token ID" : token_id_col, "Image File" : image_col, "Name" : name_col, "Description" : desc_col, "External URL" : url_col, "Attributes" : attributes_col})
	df.to_csv("stolenNFT.csv", index=False)


steal_collection(collection_to_steal)












