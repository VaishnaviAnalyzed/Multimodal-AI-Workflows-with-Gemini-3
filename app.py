import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import pathlib
import textwrap


st.set_page_config(page_title='Gemini-3 LLM Bootcamp', page_icon="🤖", layout='wide')

os.environ['GEMINI_API_KEY'] = 'AIzaSyAoYdNU6QmBlEP-H7oKiHX1WFIb20-XGfE'

import google.generativeai as genai
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def get_gemini_response(input,image): 
    model = genai.GenerativeModel("models/gemini-3-flash-preview")
    
    if input != "":
        response = model.generate_content([input,image])
    else:
        response = model.generate_content(image)
        
    return response.text

st.header("🤖 Gemini-3 LLM Model")
input = st.text_input('Input Promt:', key='input')

uploaded_file = st.file_uploader("Choose an image...", type=["png","jpg","jpeg"])

image = ""
if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_container_width= True)
    
submit = st.button('Generate Response about the image using Gemini-3 LLM')
    
if submit:
    response = get_gemini_response(input,image)
    st.subheader("Gemini-3 LLM Response:")
    st.write(response)
    
    