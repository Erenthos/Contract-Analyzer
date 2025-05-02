import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import openai

# Set your OpenAI API key
openai.api_key = "your-openai-api-key"

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to extract text from DOCX
def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to summarize the text using OpenAI
def summarize_contract(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a legal assistant."},
            {"role": "user", "content": f"Summarize the following contract:\n\n{text}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Function to answer questions
def answer_question(text, question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a legal assistant."},
            {"role": "user", "content": f"Based on the following contract:\n\n{text}\n\nAnswer the question: {question}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit app
st.title("📝 Contract Analyzer (Supply/Service)")

uploaded_file = st.file_uploader("Upload your contract (PDF or DOCX)", type=["pdf", "docx"])

contract_text = ""

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension == "pdf":
        contract_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        contract_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format.")

    if contract_text:
        if st.button("📄 Generate Contract Summary"):
            with st.spinner("Summarizing..."):
                summary = summarize_contract(contract_text)
                st.subheader("📃 Contract Summary:")
                st.write(summary)

        st.subheader("❓ Ask a Question About the Contract")
        question = st.text_input("Type your question here:")
        if question:
            with st.spinner("Thinking..."):
                answer = answer_question(contract_text, question)
                st.write("💡 Answer:")
                st.write(answer)
