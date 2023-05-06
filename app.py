import streamlit as st
import json
import base64
from docx import Document
from io import BytesIO, StringIO
import pdfplumber

# Function to extract text from PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to extract text from Word
def extract_text_from_docx(file):
    docx = Document(file)
    text = '\n'.join([paragraph.text for paragraph in docx.paragraphs])
    return text

# Function to get the JSON file download link
def get_json_download_link(json_file_name):
    with open(json_file_name, 'r') as f:
        data = f.read()
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{json_file_name}">Download JSON File</a>'
    return href

def main():
    # Create text input fields for the title, author, and date
    title = st.text_input('Title')
    author = st.text_input('Author')
    date = st.date_input('Date')

    # Create a file uploader for the PDF
    uploaded_file = st.file_uploader("Upload File", type=['pdf', 'docx', 'txt'])

    # When the user clicks the 'Add Document' button, append their input to a list
    documents = []

    # Define JSON file name
    json_file_name = 'documents.json'

    if st.button('Add Document'):
        if uploaded_file is not None:
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            if uploaded_file.type == 'application/pdf':
                content = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                content = extract_text_from_docx(uploaded_file)
            elif uploaded_file.type == 'text/plain':
                content = uploaded_file.read().decode()
            documents.append({
                'title': title,
                'content': content,
                'metadata': {
                    'author': author,
                    'date': date.isoformat()  # Convert date to string in 'YYYY-MM-DD' format
                }
            })

        # Save the list of documents to a JSON file immediately after adding
        with open(json_file_name, 'w') as f:
            json.dump(documents, f)

    # Display the list of documents
    st.write(documents)

    # Add download button for the JSON file
    if st.button('Download JSON File'):
        st.markdown(get_json_download_link(json_file_name), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
