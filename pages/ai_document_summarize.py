import streamlit as st
import os
import re
from openai import OpenAI
from navigation import make_sidebar
import utils.utils as utils

# Set Streamlit page configuration
st.set_page_config(page_title="AI Document Summarize - MicroSaaS", page_icon="📰", layout="centered", initial_sidebar_state="auto", menu_items=None)
print('Loading AI Document Summarize...')

api_key = os.getenv("OPENAI_API_KEY")
# Initializing the OpenAI client with API key from Streamlit's secret storage
client = OpenAI(api_key=api_key)

make_sidebar()

st.title('AI-powered Document Summarization Tool 📰')

html_text = f"""
    <p>Upload a document (PDF or text) and select the document type for summarization.</p>
"""
st.html(html_text)

prompts = {'Scientific Article': {
    'system': 'You work for a scientific journal and are tasked with summarizing the key findings of a research article. Your goal is to provide a concise summary of the article that highlights the main contributions and results. Pay close attention to all details and ensure that the summary captures the essence of the article. Be highly suspect of all data and conclusions.',
    'user': 'Based of the following document, provide a concise summary of all meaningful aspects of the document. The information you provide should help to determine whether the document is a good fit for publication. Finally, provide commentary on whether you believe this document worthy of publication with this information '
    },
    'Medical Blood Examination': {
        'system': 'You work for a medical clinic and are tasked with summarizing the results of a patient\'s blood examination. Your goal is to provide a concise summary of the patient\'s health status based on the blood test results. Pay close attention to key metrics like cholesterol levels, blood sugar, and other relevant indicators. Be highly suspect of any abnormalities or red flags.',
        'user': 'Based on the following document, provide a concise summary of all meaningful aspects of the document. The information you provide should help to determine the patient\'s health status based on the blood test results. Finally, provide commentary on whether you believe the patient is in good health with this information '
    },
    'Other': {
        'system': 'You work as detailed reader and are tasked with summarizing the key points of a document. Your goal is to provide a concise summary of the document that captures the main ideas and arguments. Pay close attention to all details and ensure that the summary is accurate and informative. Be highly suspect of any inconsistencies or missing information with this information ',
        'user': 'Please provide a summary of the document '
    }}

uploaded_file = st.file_uploader("Upload document (PDF or text)", type=["pdf", "txt"])
document_type = st.selectbox("Select document type", options=list(prompts.keys()))

def summarize_text(text, doc_type):
    """
    Summarizes the provided text by generating an overall summary and section summaries based on the document type.

    Parameters:
    text (str): The text content to be summarized.
    doc_type (str): The type of document (e.g., "Scientific Article", "Medical Blood Examination").

    Returns:
    dict: A dictionary containing the overall summary and summaries for each section.
    """

    # Generate an overall summary for the entire document
    overall_summary = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': prompts[doc_type]['system']},
            {'role': 'user', 'content': prompts[doc_type]['user'] + text},
        ],
        model="gpt-4-1106-preview",
    )

    summaries = {"overall_summary": overall_summary.choices[0].message.content, "section_summaries": []}

    return summaries

if st.button('Summarize') and uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        if file_type in ['pdf', 'txt']:
            text = utils.read_pdf(uploaded_file) if file_type == 'pdf' else str(uploaded_file.read(), 'utf-8')
            summaries = summarize_text(text, document_type)

            if summaries:
                st.header("Overall Summary")
                st.write(summaries["overall_summary"])  # Display the overall summary
            else:
                st.error("Failed to generate summaries.")
        else:
            st.error("Unsupported file type. Please upload a PDF or text file.")
else:
    st.info("Please upload a document to start summarization.")