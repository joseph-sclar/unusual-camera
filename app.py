import streamlit as st
from functions import generate_future_scenario, generate_images
import requests
from tempfile import NamedTemporaryFile

# App layout with improved structure and user guidance
st.title("Unusual Camera")

# API Key (should ideally be stored securely)
api_key = "bf1b8993-25c5-4d19-9eba-6095ec283b78"

# Main content area for user interaction
st.subheader("Capture Your Moment")

# Option to upload image from the device or take a new picture
upload_option = st.radio("Choose your image source:", ("Upload Image", "Take a Picture"))

if upload_option == "Upload Image":
    uploaded_image = st.file_uploader("Upload your image", type=["jpg", "png", "jpeg"])
else:
    taken_image = st.camera_input("Take a picture")

# Ensuring an image is provided either by upload or camera
image = uploaded_image if upload_option == "Upload Image" else taken_image

### PICTURE GENERATION ###

st.markdown("""---""")

st.subheader("Print the future")
character = st.text_input("Who is in the picture?")

# Scenario selection
scenario_option = st.radio("Choose your scenario type:", ("Random Future Scenario", "Custom Prompt Scenario"))

if scenario_option == "Custom Prompt Scenario":
    user_prompt = st.text_input("Enter your prompt for the custom scenario")
else:
    user_prompt = None
    
    
### SHOWING IMAGE ###



# Button to generate the image or scenario
if st.button('Generate Image/Scenario') and image:
    
    st.markdown("""---""")    
    
    with st.spinner('Creating your future glimpse...'):
        
        if scenario_option == "Custom Prompt Scenario":
            response = generate_images(api_key, character, image, user_prompt)  # Custom prompt
        else:
            response = generate_images(api_key, character, image, user_prompt)  # Random scenario

        if response:
            image_url = response[0]
            st.image(image_url, caption=response[1])

            # Download the image from the URL
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                # Save the image to a temporary file
                with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    tmp_file.write(img_response.content)
                    tmp_file_path = tmp_file.name

                # Add a download button using the temporary file
                with open(tmp_file_path, "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file,
                        file_name="generated_image.jpg",
                        mime="image/jpeg"
                    )
            else:
                st.error("Unable to download the image for saving. Please try again.")
        else:
            st.error("Unable to generate. Please check your inputs or try again later.")

st.write("Explore different scenarios by retaking pictures or uploading different images!")




