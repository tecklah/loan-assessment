import re
import os
import constants
from dotenv import load_dotenv
from util.doc_util import load_pdf_file, text_split
from util.log_util import print_message, print_documents
from rag import RAG
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv('OPENAI_API_KEY'),
    model="gpt-4.1",
    temperature=0.1,
    max_tokens=512,
)

def test_interest_rate(input: str):
    assert "medium" in input.lower(), "Result does not contain 'Medium'"
    assert re.search(r"\d+\.\d{3}\s?%", input, re.IGNORECASE), "Result does not contain a percentage like 'x.xxx %'"

def test_overall_risk(input: str):
    assert "medium" in input.lower(), "Result does not contain 'Medium'"

for rag in [{
    'doc_file_path': './docs/Bank Loan Interest Rate Policy.pdf',
    'collection_name': constants.RAG_COLLECTION_LOAN_INTEREST_RATES,
    'question': "What is the interest rate for Medium risk?",
    'test_func': test_interest_rate
}, {
    'doc_file_path': './docs/Bank Loan Overall Risk Policy.pdf',
    'collection_name': constants.RAG_COLLECTION_LOAN_OVERALL_RISK_POLICY,
    'question': "What is the risk when credit score is 455 and account status is good-standing.",
    'test_func': test_overall_risk
}]:

    print_message(f"Testing RAG for collection: {rag['collection_name']}")

    data = load_pdf_file(file_path=rag["doc_file_path"])
    documents = text_split(data, chunk_size=200, chunk_overlap=50)

    vector_store = RAG(
        llm,
        documents=documents,
        collection_name=rag["collection_name"],
        reload_collection=False
    )

    query_result, retrieved_contexts = vector_store.query(
        rag['question'],
        top_k=3
    )

    print(f"Query: {rag['question']}")
    print(query_result)

    if 'test_func' in rag:
        rag['test_func'](query_result)
