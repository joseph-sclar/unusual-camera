# functions.py

import random
import requests
import json
import time

# Your existing generate_future_scenario function
def generate_future_scenario(characters):
    
    
    
    locations = [
    "a sun-drenched Mediterranean beach",
    "a dense Amazon rainforest",
    "the summit of a snow-capped mountain",
    "a sprawling desert oasis",
    "an ancient castle ruins",
    "a serene lakeside at dawn",
    "a colorful coral reef underwater",
    "a bustling fish market",
    "a vibrant autumn forest",
    "a misty mountain valley",
    "a traditional tea garden",
    "a high-tech robotics laboratory",
    "a cozy mountain cabin",
    "a futuristic space station",
    "a lively carnival at night",
    "a serene Zen garden",
    "an old vineyard in the countryside",
    "a mystical wizard's library",
    "a hidden cave with glowing crystals",
    "a luxury yacht on the open sea",
    "a quiet monastery in the hills",
    "an underground city",
    "a neon-lit arcade room",
    "a medieval tournament ground",
    "a busy subway station",
    "a mysterious abandoned amusement park",
    "a high-speed train traversing a bridge",
    "a rooftop garden in a modern city",
    "an exotic spice market",
    "a futuristic car showroom",
    "a peaceful bamboo forest",
    "a large observatory under the stars",
    "a bustling airport terminal",
    "a large sports stadium during a game",
    "a grand museum hall",
    "an ice hotel",
    "a rural farm at sunrise",
    "a lavish masquerade ball",
    "a quiet riverside village",
    "a large library with ancient books",
    "a busy kitchen in a 5-star restaurant",
    "a tranquil underwater cave",
    "a lush vine-covered ancient ruin",
    "a classic diner on Route 66",
    "a whimsical treehouse village",
    "a modern art gallery",
    "an old wooden pier at sunset",
    "a vibrant flower garden in spring",
    "a snowy alpine skiing village",
    "a steampunk inventor's workshop"
]


    states = [
    "while it is experiencing a gentle sunrise",
    "during a sudden, mysterious fog",
    "as a futuristic solar eclipse occurs",
    "while a rare, colorful aurora lights the sky",
    "during an unexpected, vivid rainbow appearance",
    "as a group of explorers discovers a hidden path",
    "while a large, peaceful protest is happening",
    "during a sudden, intense meteor shower",
    "as an advanced alien spacecraft lands nearby",
    "while it's being restored by a team of historians",
    "during a vibrant, traditional festival",
    "as it undergoes a sudden, apocalyptic event",
    "while a group of scientists conducts a groundbreaking experiment",
    "during a historical reenactment event",
    "as a time traveler arrives from the future",
    "while a rare, exotic animal is spotted",
    "during a sudden, powerful thunderstorm",
    "as a massive, futuristic city is being constructed in the background",
    "while a group of children discover a magical artifact",
    "during a serene, beautiful full moon night",
    "as a group of artists creates a massive mural",
    "while a high-speed chase unfolds",
    "during a massive, peaceful candlelight vigil",
    "as it becomes the site of a groundbreaking archaeological find",
    "while a futuristic sports event is taking place",
    "during an intense, unexpected blizzard",
    "as a group of survivors navigates a post-apocalyptic world",
    "while a grand wedding celebration is happening",
    "during a large-scale, futuristic environmental rejuvenation project",
    "as it becomes the center of a global peace summit",
    "while a mysterious, ancient ritual is being reenacted",
    "during a lavish, futuristic fashion show",
    "as it's transformed into a utopian society",
    "while a group of researchers uncovers a new technological breakthrough",
    "during a sudden, mystical portal opening",
    "as it serves as a backdrop for a classic car rally",
    "while it is being visited by a group of time-traveling tourists",
    "during a major, global virtual reality event",
    "as a new, sustainable energy source is being inaugurated",
    "while a group of adventurers sets off on an epic journey",
    "during a catastrophic natural disaster",
    "as it becomes a refuge for an endangered species",
    "while a film crew shoots a blockbuster movie",
    "during a large, joyous outdoor concert",
    "as it becomes a hub for interstellar travel",
    "while a groundbreaking peace treaty is being signed",
    "during a unique, otherworldly phenomenon",
    "as a secret, underground society is revealed",
    "while it hosts an international culinary festival",
    "during a spectacular, futuristic air show"
    ]




    # Select one item randomly from each list
    random_location = random.choice(locations)
    random_state = random.choice(states)

    # Combine the selections into a single prompt
    prompt = f"{characters} in {random_location} {random_state}."
    return prompt



def generate_images(api_key, characters, taken_image, user_prompt):


    image_data = None

    if taken_image is not None:
        image_data = taken_image.getvalue()

        
        
    if image_data is not None:
        # Save the image
        with open("image.png", "wb") as f:
            f.write(image_data)

        authorization = "Bearer %s" % api_key
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": authorization
        }

        # Get a presigned URL for uploading an image
        url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
        payload = {"extension": "png"}
        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code)

        # Upload image via presigned URL
        fields = json.loads(response.json()['uploadInitImage']['fields'])
        url = response.json()['uploadInitImage']['url']
        image_id = response.json()['uploadInitImage']['id']

        image_file_path = "image.png"  # Updated to use the saved image
        files = {'file': open(image_file_path, 'rb')}
        response = requests.post(url, data=fields, files=files)
        print(response.status_code)

        # Generate with an image prompt
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        
        if user_prompt:
            prompt = user_prompt
            pass
        else:
            prompt =  generate_future_scenario(characters)


        payload = {
            "alchemy": True,
            "presetStyle": "PHOTOGRAPHY",
            "highResolution": True,
            "guidance_scale": 7,
            "height": 512,
            "photoReal": True,
            "num_images": 1,
            "public": False,
            "init_strength" : .35,
            "imagePromptWeight": 7, 
            #"modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", # Setting model ID to Leonardo Creative
            "prompt": prompt,
            "width": 512,
            "init_image_id": image_id,
            "negative_prompt": "Do not change the gender, ethnicity, skin color or race",
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.status_code)
        print(response.json())

        # Get the generation of images
        generation_id = response.json()['sdGenerationJob']['generationId']

        url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

        time.sleep(20)

        response = requests.get(url, headers=headers)
        
        # Convert to dictionary
        response_dict = json.loads(response.text)

        # Extract the URL
        url = response_dict['generations_by_pk']['generated_images'][0]['url']

        
        return url, prompt
