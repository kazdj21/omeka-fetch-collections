import requests
import json
import re
import string

hasReachedEnd = False
encounteredEmptyCollection = 0
i = 1
lastID = 1
count = 0

print("Welcome!")
print("Please input the collections endpoint from your Omeka API.")
print("Example: https://uogguafak.omeka.net/api/collections/")
url = input("Input the URL here: ")
print("Now generating a collections_output.csv")
with open("collections_output.csv", "w") as file:
    file.write("id, url, public, featured, added, modified, collection_name, collection_description \n")
    while not hasReachedEnd:
        generated_url = url + str(i)
        res = requests.get(generated_url)
        data = json.loads(res.text)
        if 'message' in data.keys():
            if data['message'] == "Invalid record. Record not found.":
                encounteredEmptyCollection += 1
                if encounteredEmptyCollection > 10:
                    hasReachedEnd = True
                    break
        else:

            # Columns
            id = data['id']
            user_url = data['url']
            public = data['public']
            featured = data['featured']
            added = data['added']
            modified = data['modified']
            collections_name = ""
            collections_description = ""

            if 'element_texts' in data.keys():
                if 'text' in data['element_texts'][0].keys():
                    # collections_name = data['element_texts'][0]['text']
                    collections_name = re.sub(f'[{re.escape(string.punctuation)}\n\r\t]', ' ', data['element_texts'][0]['text'])

            if 'element_texts' in data.keys():
                if len(data['element_texts']) > 1:
                    if 'text' in data['element_texts'][1].keys():
                        # collections_description = data['element_texts'][1]['text']
                        collections_description = re.sub(f'[{re.escape(string.punctuation)}\n\r\t]', ' ', data['element_texts'][1]['text'])

            print(f"{id}, {user_url}, {public}, {featured}, {added}, {modified}, {collections_name}, {collections_description} \n")
            file.write(f"{id}, {user_url}, {public}, {featured}, {added}, {modified}, {collections_name}, {collections_description} \n")
            lastID = i
            encounteredEmptyCollection = 0
            count += 1

        i += 1

print(f"Last ID of collection: {lastID}")
print(f"Number of collections: {count}")

