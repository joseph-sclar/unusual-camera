# functions.py

import random
import requests
import json
import time

# Your existing generate_future_scenario function
def generate_future_scenario(characters):
    
    
    
    locations = [
        "a futuristic city", "Berlin", "Paris", "a space station", "Mars", "Spaceship", 
        "a city full of neon lights", "rustic village with futuristic buildings", "a floating island in the sky", 
        "an underwater city", "a desert oasis with advanced technology", "futuristic living room", "crowded place",
        "a cyberpunk metropolis", "a high-tech jungle village", "a lunar base on the Moon", "Saturn", "Apocalypse", 
        "by the ocean", "Mexico", "Cancun", "an interstellar travel port", "a futuristic mountain retreat", 
        "an ancient city with advanced alien technology", 
        "a high-tech arctic research station", "a holographic entertainment center", "a luxury space cruise", 
        "a digital landscape in a computer network", "a post-apocalyptic urban jungle", "a quantum computation center", 
        "an eco-friendly city powered by renewable energy", "a hidden village with advanced cloaking technology", 
        "a megacity with towering skyscrapers and flying cars", "an interdimensional gateway city", "a time-travel hub", 
        "a solar-powered city in the Sahara", "a utopian society on a remote island", "a biotech innovation center in Silicon Valley",
        "New York", "Tokyo", "London", "Sydney", "Rome", "Cape Town", "Shanghai", "Moscow", "Los Angeles", "Toronto",
        "San Francisco", "Amsterdam", "Singapore", "Bangkok", "Dubai", "Rio de Janeiro", "Mumbai", "Seoul", "Istanbul", "Lisbon"
    ]


    states = [
        "overgrown with lush, wild nature", 
        "bathed in vibrant neon lights", 
        "crumbling under the aftermath of an alien invasion", 
        "enveloped in a gentle, persistent rain", 
        "buzzing with sleek, advanced futuristic technology", 
        "illuminated by a constant, mesmerizing aurora borealis", 
        "basking in bright, cheerful sunshine", 
        "covered in a blanket of soft, pristine snow", 
        "desolate streets with remnants of a zombie apocalypse", 
        "alive with colorful lights and decorations of a futuristic festival", 
        "radiating the warm glow of a summer day", 
        "under attack, with alien spacecraft looming in the sky", 
        "frozen in the depths of an ice age, with glaciers and snowdrifts", 
        "darkened under the shadow of a solar eclipse", 
        "chaotic with rampaging robots among city ruins", 
        "tranquil in a snow-covered winter landscape", 
        "sweltering under an intense, scorching heatwave", 
        "dramatic with frequent lightning and thunderstorms", 
        "carpeted in autumn leaves during a fall setting", 
        "transforming rapidly in a technological revolution", 
        "peaceful and serene, perhaps with gentle streams or quiet fields", 
        "bustling with people in historical costumes during a reenactment", 
        "mysteriously shrouded in a thick, mystical fog", 
        "undergoing dramatic environmental changes due to climate shift", 
        "festive and lively during a grand music festival", 
        "exciting and crowded during a major sports event", 
        "submerged in water, post-flood, with buildings partially underwater", 
        "intense and fiery during a volcanic eruption", 
        "thriving in an economic boom, with signs of prosperity and growth", 
        "vibrant and artistic during a cultural futuristic renaissance", 
        "tense and charged during a political revolution in the near future",  
        "eerie with subtle signs of alien observation in the sky", 
        "quiet and isolated in a state of quarantine", 
        "creative and colorful in the midst of an art movement", 
        "dark and mysterious during a citywide blackout", 
        "spectacular with supernatural phenomena like ghostly apparitions or floating orbs",
        "busy with rush hour traffic in a modern city", 
        "calm and reflective during a beautiful sunset", 
        "energetic and vibrant in a bustling city market", 
        "serene and pastoral in a rural countryside setting with flying cars", 
        "soaked in a heavy downpour during a monsoon season",
        "foggy and mysterious in an early morning mist"
    ]




    # Select one item randomly from each list
    random_location = random.choice(locations)
    random_state = random.choice(states)

    # Combine the selections into a single prompt
    prompt = f"{characters} in {random_location} while it is {random_state}."
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
            "presetStyle": "CINEMATIC",
            "contrastRatio": 0,
            "highResolution": True,
            "guidance_scale": 7,
            "height": 512,
            "num_images": 1,
            "public": False,
            "init_strength" : .3,
            "imagePromptWeight": 7, 
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", # Setting model ID to Leonardo Creative
            "prompt": prompt,
            "width": 512,
            "init_image_id": image_id
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
