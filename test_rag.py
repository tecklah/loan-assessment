import re
import constants
from dotenv import load_dotenv
from util.doc_util import load_pdf_file, text_split
from util.log_util import print_message, print_documents
from rag import RAG

load_dotenv()

def test_interest_rate(input: str):
    assert "medium" in input.lower(), "Result does not contain 'Medium'"
    assert re.search(r"\d+\.\d{3}\s?%", input, re.IGNORECASE), "Result does not contain a percentage like 'x.xxx %'"

def test_overall_risk(input: str):
    credit_score = 455
    assert "medium" in input.lower() and 'good-standing' in input.lower(), "Result does not contain 'Medium' or 'Good-standing'"
    ranges = re.findall(r'(\d+)\s*[–-]\s*(\d+)', input)
    in_range = any(int(start) <= credit_score <= int(end) for start, end in ranges)
    assert in_range, f"{credit_score} is not in any range in the output"

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
        documents=documents,
        collection_name=rag["collection_name"],
        reload_collection=True
    )

    query_result, retrieved_contexts = vector_store.query(
        rag['question'],
        top_k=3
    )

    print(f"Query: {rag['question']}")
    print(query_result)

    if 'test_func' in rag:
        rag['test_func'](query_result)
