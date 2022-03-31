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
import json as JSON
import sys
import fileinput
import urllib.parse as urlparse

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
target_path ='./collections'

#Function to save NFT as files
def write_text(data: bytes, path: str):
    with open(path, 'wb') as file:
        file.write(data)

#Function to get the api url that displays the json data
def get_json_url(contract_add, token_id,collection_to_steal):
    links = []

    #Construct the asset url of the indivual nft
    asset_url = "https://opensea.io/assets/" + contract_add + "/" + token_id

    #Scrape the asset url to get the api url
    req = Request(asset_url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")

    #Scraping all the urls in the page
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    #Getting the unique key of the collection
    for link in links:
        if link != None and str(token_id) in link:
            #print(link)

            return link


def steal_collection(collection_url: str):
    links = []
    json_list = []
    scrapped_json = []
    image_list = []
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
                token_id = link.rsplit('/', 1)[-1]

    acquired_json_url = get_json_url(str(contract_address.group(1)), str(token_id),collection_url)

    #Check for file extension
    ext = os.path.splitext(urlparse.urlparse(acquired_json_url).path)[1]


    json_url = os.path.dirname(acquired_json_url)


    #Specify the range of NFTs
    i = int(token_id)
    while i < int(token_id)+10:
        if ext != None:
            unique_json_url = json_url + '/' + str(i) + ext
        else:
            unique_json_url = json_url + '/' + str(i)
        json_list.append(unique_json_url)
        i+=1

    #get all json data
    for json in json_list:
        r = requests.get(json)
        scrapped_json.append(r)

    j=0
    for json_element in scrapped_json:
        
        #Convert response to json
        json_object = json_element.json()
        found_image = json_object["image"]

        #IF incomplete image url
        if found_image.startswith("ipfs://"):
            image_list.append(found_image)
            found_image = found_image.replace("ipfs://", "https://ipfs.io/ipfs/")
        else:
            image_list.append(found_image)

        


        #Conovert json to string
        json = str(json_element.json())


        #Create collections folder if doesnt exist
        target_path = './collections'
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        #Create unique collection folder to store image and json folder
        # ./collections/collection_name
        target_folder = os.path.join(target_path,'_'.join(collection_name.lower().split(' ')))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        #Create image folder in collections/collection_name/
        # ./collections/collection_name/images
        image_path = os.path.join(target_folder,"images")
        
        if not os.path.exists(image_path):
            os.makedirs(image_path)


        #Download images from image link and store in /collections/collection_name/image
        svg = requests.get(found_image).content
        filename = image_path + "/" +found_image.rsplit('/', 1)[-1]
        write_text(svg, filename)


        #Path to store json files
        json_path = os.path.join(target_folder,"json")
        if not os.path.exists(json_path):
            os.makedirs(json_path)

        json_file_path = json_path + "/" + str(j)

        #Write json into files to be uploaded onto ipfs
        with open(json_file_path, 'w') as f:
            f.write(json)
        j+=1

    return(image_list)



def replace_imagelink_json(collection_name, CID_image,image_list):
    #https://gateway.pinata.cloud/ipfs/QmSps8bjjbyKnCx4CWXzoBz4Sb4fT6ba1i4e5rqYByEwtf/images

    #Get number of files in json directory
    dir_path = './collections/'+collection_name+'/json'

    #Count number of files in json directory
    path, dirs, files = next(os.walk(dir_path))
    file_count = len(files)


    i=0
    while i<file_count:
        new_string = "https://gateway.pinata.cloud/ipfs/" + CID_image + "/" + image_list[i].rsplit('/', 1)[-1]

        json_file = dir_path+"/"+str(i)


        x = image_list[i]
        y = new_string
             
        with open(json_file, 'r+') as file:
            for l in fileinput.input(files = json_file):
                l = l.replace(x, y)
                #sys.stdout.write(l)
                
                file.write(l)

        i+=1

    

#Driver code

result = steal_collection(collection_to_steal)

print("We've gotten the goods! Upload them to IPFS!")

CID_images = input("Enter the CID for images: ")

replace_imagelink_json(collection_name, CID_images,result)

print("The json files are ready at /collections/"+collection_name+"/json")
