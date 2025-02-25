import streamlit as st
from dotenv import load_dotenv
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process uploaded PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App
st.set_page_config(page_title="Resume Analyzer")

# Custom CSS to style the logo, add a subtitle, and set a white background
st.markdown(
    """
    <style>
    /* Set white background for the entire app */
    body {
        background-color: white !important;
        color: black !important; /* Ensure default text color is black */
    }

    /* Ensure Streamlit components have a white background */
    .stApp {
        background-color: white;
        color: black; /* Ensure text in Streamlit components is black */
    }

    /* Style headers and titles */
    h1, h2, h3, h4, h5, h6 {
        color: black !important; /* Ensure headers are black */
    }

    /* Style the logo */
    .logo {
        width: 150px; /* Adjust the size as needed */
        height: auto;
        margin-top: -50px; /* Adjust positioning */
    }

    /* Style the subtitle */
    .subtitle {
        font-size: 14px;
        color: #333; /* Dark gray for better visibility */
        margin-top: -30px; /* Reduce space after header */
    }

    /* Style Streamlit text areas and input fields */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        color: black !important; /* Ensure input text is black */
        background-color: white !important; /* Ensure input background is white */
    }

    /* Style buttons */
    .stButton>button {
        background-color: #4a90e2; /* Blue background for buttons */
        color: white !important; /* White text for buttons */
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
    }
    
    
   
    """,
    unsafe_allow_html=True,
)

# Add logo using custom HTML
st.image("logo.png" ,width= 150)

# App header
st.header("ATS Tracking System")

# Subtitle below "ATS Tracking System"
st.markdown('<p class="subtitle">Developed by Ayush Raut</p>', unsafe_allow_html=True)

# Input fields
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

# Prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage, then keywords missing, and finally, your final thoughts.
"""

# Handle button clicks
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")