import os
from dotenv import load_dotenv
import google.generativeai as genai
import pathlib
import textwrap


## Loading API key
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')


## Configuring llm with API key
genai.configure(api_key=API_KEY)


## Loading gemini-pro model
def load_gemini_model():
    model = genai.GenerativeModel('gemini-pro')
    return model


## Function for image captioning
def load_gemini_vision_model_response(prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if prompt != "":
        response = model.generate_content([image, prompt])
    else:
        response = model.generate_content(image)
    return response.text



## Function to get embeddings
def embeddings_model_response(text):
    embedding_model = 'models/text-embedding-004'
    embeddings = genai.embed_content(
        model=embedding_model,
        content=text,
        task_type='retrieval_document'
    )
    return embeddings['embedding']



## Function to get response
def get_response(text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(text)
    return response.text