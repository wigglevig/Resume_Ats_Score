from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import fitz
import google.generativeai as genai

# Load API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_response(input_text, pdf_content, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([input_text, pdf_content, prompt])
        return response.text
    except Exception as e:
        return f"Error in generating response: {e}"

@st.cache_data
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text_parts = [page.get_text() for page in document]
            pdf_text_content = " ".join(text_parts)
            return pdf_text_content
        except Exception as e:
            st.error(f"Error in processing PDF: {e}")
            return None
    else:
        st.error("No file uploaded")
        return None

## Streamlit App
st.set_page_config(page_title="Resume Expert")

st.header("Resume ATS Expert")
st.subheader("This application helps you review your resume with the help of Google's GEMINI AI [LLM]")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])
input_text = st.text_area("Job Description(from linkedIn/website):", key="input")

pdf_content = ""

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve my Skills")
submit3 = st.button("What are the Keywords That are Missing")
submit4 = st.button("Percentage Match")
input_promp = st.text_input("Queries: Feel Free to Ask Here")
submit5 = st.button("Answer My Query")

input_prompt1 = """
You are an experienced Senior Technical Human Resource Manager. Your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a Senior Technical Human Resource Manager with expertise in data science. 
Your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective. 
Additionally, offer advice on enhancing the candidate's skills and identify areas where improvement is needed.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. As a Senior Human Resource manager,
assess the compatibility of the resume with the role. Identify the missing keywords and provide recommendations for enhancing 
the candidate's skills and areas requiring further development.
"""

input_prompt4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match of the resume with the job description,
followed by the missing keywords, and then your final thoughts.
"""

if submit1 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    if pdf_content:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)

elif submit2 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    if pdf_content:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("The Response is")
        st.write(response)

elif submit3 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    if pdf_content:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)

elif submit4 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    if pdf_content:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.subheader("The Response is")
        st.write(response)

elif submit5 and uploaded_file is not None:
    pdf_content = input_pdf_setup(uploaded_file)
    if pdf_content:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_promp, pdf_content, input_promp)
        st.subheader("The Response is")
        st.write(response)

footer = """
---
#### Made By [Vignesh](https://www.linkedin.com/in/vigneshpandi0908/)
For Queries, Reach out on [LinkedIn](https://www.linkedin.com/in/vigneshpandi0908/)  
*Resume ATS Expert - Making Job Applications Easier*
"""
st.markdown(footer, unsafe_allow_html=True)
