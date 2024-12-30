import streamlit as st
from PIL import Image
from langchain.schema import StrOutputParser
from langchain_ollama import ChatOllama
from utils import convert_to_base64, prompt_func
import pprint


# Page configuration
st.set_page_config(
    page_title="Llama 3.2 Vision",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
st.title("🦙 Chat with your document")

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        if 'response' in st.session_state:
            del st.session_state['response']
        st.rerun()

#st.markdown('<p style="margin-top: -20px;">Llama 3.2 Vision!</p>', unsafe_allow_html=True)
#text = st.text_area('Enter Text Below (maximum 800 words):', height=300) 

question = st.text_input("Enter question (maximum 800 words):", None)

if question:
    st.session_state['question'] = question
    #st.write("Input text:", st.session_state['question'])    

st.markdown("---")
# Move upload controls to sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    st.markdown("---")
    
    if uploaded_file is not None:

        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        
        if 'question' in st.session_state:
            # with st.spinner("Processing image..."):
                # try:
                llm = ChatOllama(model="llama3.2-vision", temperature=0)
                image_b64 = convert_to_base64(image)

                chain = prompt_func | llm | StrOutputParser()

                text = f"""
                    You will be provided with an image of a document. 
                    Your task is to answer the user question. 
                    If you are unable to answer the question, please do not come up with a random answer.     
                    Question: {st.session_state['question']}
                    """

                query_chain = chain.invoke(
                    {
                    "text": text, 
                    "image": image_b64
                    }
                )

                pprint.pprint(query_chain)

                st.session_state["response"] = query_chain

                # except Exception as e:
                #     st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'response' in st.session_state:
    st.markdown("**Response:**")
    st.write(st.session_state["response"])
    
    # st.markdown("### LaTeX Code")
    # st.code(st.session_state['ocr_result'], language='latex')

    # st.markdown("### LaTeX Rendered")

    # cleaned_latex = st.session_state['ocr_result'].replace(r"\[", "").replace(r"\]", "")
    # st.latex(cleaned_latex)
# else:
#     st.info("Upload an image first.")
