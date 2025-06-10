import streamlit as st
import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize Gemini model with safety settings
generation_config = {
    "temperature": 0.75,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_pdf_summary(pdf_text):
    """Get a summary of the PDF content."""
    try:
        prompt = f"""Please provide a comprehensive summary of the following text. 
        Focus on the main points, key arguments, and important details. 
        Format the summary in a clear and organized way:

        {pdf_text[:10000]}  # Limiting text length for summary
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return "Failed to generate summary. Please try again."

def get_gemini_response(prompt, pdf_text):
    """Get response from Gemini model."""
    try:
        context = f"Context from PDF: {pdf_text}\n\nQuestion: {prompt}"
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        st.error(f"Error getting response from Gemini: {str(e)}")
        return "I apologize, but I encountered an error while processing your request. Please try again."

# Set page config
st.set_page_config(page_title="PDF Chat with Gemini", page_icon="📚")

# Title
st.title("📚 PDF Chat with Gemini")
st.write("Upload a PDF and get an instant summary, then ask questions about its content!")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    # Initialize session state for summary and chat
    if "summary" not in st.session_state:
        with st.spinner("Generating summary..."):
            st.session_state.summary = get_pdf_summary(pdf_text)
    
    # Display the summary
    st.subheader("📝 PDF Summary")
    st.write(st.session_state.summary)
    
    st.divider()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the PDF"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt, pdf_text)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Please upload a PDF file to start! The system will first provide a summary, then you can ask questions about the content.") 