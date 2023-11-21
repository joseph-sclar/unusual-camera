import streamlit as st
from functions import generate_future_scenario, generate_images

            
            # App layout with improved structure and user guidance
st.title("Unusual Camera")

# API Key (should ideally be stored securely)
api_key = "bf1b8993-25c5-4d19-9eba-6095ec283b78"


# Main content area for user interaction
st.header("Capture Your Moment")
taken_image = st.camera_input("Take a picture")

st.header("Identify the Characters")
characters = st.text_input("Who is in the picture? Describe briefly.")

# Button to generate the image
if st.button('Generate Futuristic Image'):
    with st.spinner('Creating a glimpse into the future...'):
        # Assuming generate_images is a defined function
        
        response = generate_images(api_key, characters, taken_image)
        
        image_url = response[0]

        # Displaying the generated image or an error message
        if image_url:
            st.image(image_url, caption=response[1])
        else:
            st.error("Unable to generate image. Please check your inputs or try again later.")

st.write("Explore different scenarios by retaking pictures!")


