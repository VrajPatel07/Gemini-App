import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

from gemini_utility import load_gemini_model
from gemini_utility import load_gemini_vision_model_response
from gemini_utility import embeddings_model_response
from gemini_utility import get_response


## Setting up the page configuration
st.set_page_config(
    page_title='Gemini AI',
    layout='centered'
)


with st.sidebar:
    selected = option_menu(
        menu_title='Gemini AI',
        options=['ChatBot', 'Image Captioning', 'Embed text','Ask anything'],
        menu_icon='robot',
        icons=['chat-dots-fill', 'image-fill', 'textarea-t','patch-question-fill'],
        default_index=0
    )



## Function to translate role between llm and streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role




if selected == 'ChatBot':

    model = load_gemini_model()

    ## Initialize chat session
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title('ChatBot')

    ## Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    ## Input fiels
    user_prompt = st.chat_input('Ask...')
    
    if user_prompt:
        st.chat_message('user').markdown(user_prompt)
        response = st.session_state.chat_session.send_message(user_prompt)

        ## Display response
        with st.chat_message('assistant'):
            st.markdown(response.text)



if selected == 'Image Captioning':

    st.title('Snap Narrate')

    prompt = st.text_input(label='Prompt...')
    uploaded_image = st.file_uploader('Upload an image...', type=['jpg', 'png', 'jpeg'])

    image = None   
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Generate")

    if submit and image is not None:
        response = load_gemini_vision_model_response(prompt, image)
        st.markdown(response)



if selected == 'Embed text':
    
    st.title("Embed Text")

    input_text = st.text_area(label='', placeholder='Enter the text to get embeddings')

    if st.button('Get Embeddings') and input_text:
        response = embeddings_model_response(input_text)
        st.markdown(response)



if selected == 'Ask anything':

    st.title('Ask me a Question')

    prompt = st.text_input(label='', placeholder='Ask Gemini....')

    if st.button('Ask') and prompt:
        response = get_response(prompt)
        st.markdown(response)