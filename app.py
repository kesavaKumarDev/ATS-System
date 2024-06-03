from dotenv import load_dotenv

load_dotenv()

import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

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

## Streamlit App

st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    


submit1 = st.button("Tell Me About the Resume")

#submit2 = st.button("How Can I Improvise my Skills")

submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the resume")




# import base64
# import streamlit as st
# import os
# import io
# from PIL import Image
# import pdf2image
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Set page configuration
# st.set_page_config(page_title="ATS Resume Expert" )

# # Google API Key configuration
# api_key = os.getenv('GOOGLE_API_KEY')
# if api_key is None:
#     st.error("API key not found. Please check your .env file.")
# else:
#     try:
#         genai.configure(api_key=api_key)
#     except Exception as e:
#         st.error(f"Failed to configure API key: {e}")

# # File uploader for PDF files
# uploaded_file = st.file_uploader("Upload your resume (PDF)...")

# if uploaded_file is not None:
#     # Process the uploaded file
#     st.write("Processing the uploaded PDF file...")
#     try:
#         # Convert PDF to images using pdf2image
#         images = pdf2image.convert_from_bytes(uploaded_file.read())
#         for i, image in enumerate(images):
#             st.image(image, caption=f'Page {i+1}', use_column_width=True)

#         # Example of using Google Generative AI
#         # This is a placeholder example; replace with actual usage
#         try:
#             response = genai.some_function()  # Replace with actual function
#             st.write("API response:", response)
#         except Exception as api_error:
#             st.error(f"API request failed: {api_error}")

#     except Exception as e:
#         st.error(f"Error processing the PDF file: {e}")
