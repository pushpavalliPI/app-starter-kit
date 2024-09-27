from dotenv import load_dotenv
load_dotenv()  # Load the env vars from .env
import streamlit as st
import os  # Picking up env vars
from PIL import Image
import google.generativeai as genai

# Set up the API key for the Gemini model
genai.configure(api_key=os.getenv("GENAI_API_KEY"))  # Use env variable

# Function to load gemini pro vision
def get_gemini_response(prompt):
    response = genai.generate_text(
        prompt=prompt  # Correct parameter name
    )
    return response.candidates[0]['output']  # Extracting the response text

# Function to handle image uploads
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.sidebar.header("RoboBill 🦾")
st.sidebar.write("Made by Shambhavi Tiwari.")
st.sidebar.write("Assistant used is Gemini Pro Vision.")
st.header("RoboBill 🦾")
st.subheader("Manage your expenses with the help of the robot!")

# User input and image upload
input_text = st.text_input("What do you want me to do?", key="input")
uploaded_file = st.file_uploader("Choose an image.", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Predefined prompt for Gemini API
input_prompt = f"""
You are an expert in understanding invoices.
We will upload an image as invoices, and you will have to answer any questions based on the uploaded invoice image.
User's request: {input_text}
Make sure to greet the user first and then provide the information as suited.
Make sure to keep the font uniform and give the items list in a point-wise format.
At the end, make sure to repeat the name of our app "RoboBill 🦾" and ask the user to use it again.
"""

# Button click event
if st.button("Let's go!"):
    if uploaded_file:
        image_data = input_image_details(uploaded_file)
        # Generate response using the Gemini API
        response_text = get_gemini_response(input_prompt)
        st.subheader("Here's what you need to know:")
        st.write(response_text)
    else:
        st.error("Please upload an image first!")
