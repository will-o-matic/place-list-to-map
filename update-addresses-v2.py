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
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

# Function to refine the business name using GPT-3
def refine_name_with_gpt3(name):
    max_attempts = 3  # Set the maximum number of attempts here
    for attempt in range(max_attempts):
        try:
            response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You are an AI assistant who always answers directly and does not ask follow up questions.  Your role is to act as a general purpose utility function.  When asked to answer a question, you do not add additional, unrelated text.  Simply answer the question in as few words as possible."
    },
    {
      "role": "user",
      "content": "This is a business name that may be followed by unrelated text and/or emoji: '8-Bit Bites 🎮 🍔'. Attempt to guess which part is the business name and return the name of the business enclosed in square brackets. Keep in mind that business names are not typically only one character long."
    },
    {
      "role": "assistant",
      "content": "[8]"
    },
    {
      "role": "user",
      "content": "That is incorrect. The correct output would have been [8-Bit Bytes]."
    },
    {
      "role": "assistant",
      "content": "Thank you for the clarification."
    },
    {
      "role": "user",
      "content": "Here are some additional examples to train yourself with. Input: 8-Bit Bites 🎮 🍔, Output: [8-Bit Bites]. Input: Beetle House 🎃 🍽️ 🗒️, Output: [Beetle House]. Input: T-swirl Crêpe 🥐🧁crème burlee *must go 🤩, Output: [T-Swirl Crêpe]. Input: Tompkins square bagels 🥯 🤩, Output: [Tompkins Square Bagels]."
    },
    {
      "role": "assistant",
      "content": "Thank you for the additional examples!"
    },
    {
      "role": "user",
      "content": f"This is a business name that may be followed by unrelated text and/or emoji: {name}. Attempt to guess which part is the business name and return the name of the business enclosed in square brackets."
    }
  ],
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

            responseContent = response['choices'][0]['message']['content']

            # Find the text within square brackets
            match = re.search(r'\[(.*?)\]', responseContent)

            if match:
                return match.group(1)
            else:
                return "No business name found within square brackets."

             
        except Exception as e:
            print(f"Exception occurred: {e}")
            if attempt < max_attempts - 1:  # Don't sleep on the last attempt
                print(f"Sleeping for 2 seconds before retrying...")
                time.sleep(2)
            else:
                print("Max attempts reached. Returning original name.")
                return name

# Function to get place information from Google
def get_place_info(place_name):
    # Set up the parameters for the request
    # locationbias centers the request on a specific lat/long pair
    params = {
        "query": place_name,
        "location": "40.731300,-73.989502",
        "radius": 1000,
        "key": google_api_key
    }

    # Send the request
    response = requests.get(url, params=params)

    # Parse the response
    data = response.json()

    place_info = []
    if data['status'] == 'OK':
        for candidate in data['results']:
            name = candidate['name']
            address = candidate['formatted_address']
            lat = candidate['geometry']['location']['lat']
            lng = candidate['geometry']['location']['lng']
            place_id = candidate['place_id']
            status = candidate['business_status']

            maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"

            place_info.append((name, address, status, lat, lng, maps_url))
    else:
        place_info.append((place_name, "", "", "", "", ""))

    return place_info

# Read from the text file
with open('businesses.txt', 'r', encoding='utf-8') as infile:
    businesses = infile.read().splitlines()

# Write to the CSV file
with open('business_info.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['business_name', 'refined_name_gpt', 'notes/emoji', 'address', 'status', 'latitude', 'longitude', 'Google Maps URL'])

    for business in businesses:
        business_name = re.search(r"([\w\s]*)(.*)", business).group(1).strip()
        notes_emoji = re.search(r"([\w\s]*)(.*)", business).group(2).strip()
        time.sleep(1)
        refined_name = refine_name_with_gpt3(business)
        places_info = get_place_info(refined_name)
        for name, address, status, lat, lng, maps_url in places_info:
            writer.writerow([name, refined_name, notes_emoji, status, address, lat, lng, maps_url])
