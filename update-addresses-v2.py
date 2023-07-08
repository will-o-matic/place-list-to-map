import csv
import requests
import json
import re
import openai
import time 
import json

# Load secret keys from a JSON file
with open('secrets.json') as f:
    keys = json.load(f)

openai.api_key = keys["openai_key"]
google_api_key = keys["google_key"]

# Google Places API URL
url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# Function to refine the business name using GPT-3
def refine_name_with_gpt3(name):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"This is a business name and may contain additional notes and emoji: '{name}'. Please attempt to return only the name of the business and nothing else in your response. "}
        ]
    )

    return response['choices'][0]['message']['content']

# Function to get place information from Google
def get_place_info(place_name):
    # Set up the parameters for the request
    params = {
        "input": place_name + " New York, NY",
        "inputtype": "textquery",
        "fields": "name,formatted_address,geometry,place_id",
        "key": google_api_key
    }

    # Send the request
    response = requests.get(url, params=params)

    # Parse the response
    data = response.json()

    if data['status'] == 'OK':
        name = data['candidates'][0]['name']
        address = data['candidates'][0]['formatted_address']
        lat = data['candidates'][0]['geometry']['location']['lat']
        lng = data['candidates'][0]['geometry']['location']['lng']
        place_id = data['candidates'][0]['place_id']

        maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

        return name, address, lat, lng, maps_url
    else:
        return place_name, "", "", "", ""

# Read from the text file
with open('businesses.txt', 'r', encoding='utf-8') as infile:
    businesses = infile.read().splitlines()

# Write to the CSV file
with open('business_info.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['business_name', 'notes/emoji', 'address', 'latitude', 'longitude', 'Google Maps URL'])

    for business in businesses:
        business_name = re.search(r"([\w\s]*)(.*)", business).group(1).strip()
        notes_emoji = re.search(r"([\w\s]*)(.*)", business).group(2).strip()
        time.sleep(1)
        refined_name = refine_name_with_gpt3(business_name)
        name, address, lat, lng, maps_url = get_place_info(refined_name)
        writer.writerow([name, notes_emoji, address, lat, lng, maps_url])
