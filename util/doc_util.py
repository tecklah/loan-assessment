import pdfplumber
from util.log_util import print_documents
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_pdf_file(file_path):
    '''
    Load a PDF file and extract text and tables as documents.
    '''
    documents = []
    with pdfplumber.open(file_path) as pdf:

        for page_no, page in enumerate(pdf.pages, start=1):

            text = page.extract_text()
            if text:
                documents.append(Document(
                    page_content=text,
                    metadata={"page": page_no - 1, "type": "text"}
                ))

            tables = page.extract_tables()

            for table in tables:

                header = cleanse_table_row(table[0])
                rows = table[1:]

                # Convert to Markdown table
                markdown_header = "|" + "|".join(header) + "|\n"
                markdown_header += "|" + "|".join(["---"] * len(header)) + "|\n"

                for row in rows:

                    markdown_row = markdown_header
                    markdown_row += "|" + "|".join(cleanse_table_row(row)) + "|\n"

                    documents.append(Document(
                        page_content=markdown_row,
                        metadata={"page": page_no - 1, "type": "table", "unsplittable": True}
                    ))

    # loader = PDFPlumberLoader(file_path)
    # documents = loader.load()
    # print("Loaded PDF document:", documents)

    return documents

def cleanse_table_row(row):
    '''
    Given row is a list, remove any empty string or None values and return as a new list.
    '''
    return [cell for cell in row if cell not in (None, '')]

def text_split(documents, chunk_size=100, chunk_overlap=20):
    '''
    Split documents into smaller chunks using RecursiveCharacterTextSplitter.'''
    chunks = []
    splitter = RecursiveCharacterTextSplitter.from_language(
        language="markdown", 
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )

    for doc in documents:
        if doc.metadata.get("unsplittable"):
            chunks.append(doc)
        else:
            chunks.extend(splitter.split_documents([doc]))

    print_documents(chunks)
    return chunks
