import constants
from dotenv import load_dotenv
from util.doc_util import load_pdf_file, text_split
from rag import RAG

load_dotenv()

for rag in [{
    'doc_file_path': './docs/Bank Loan Interest Rate Policy.pdf',
    'collection_name': constants.RAG_COLLECTION_LOAN_INTEREST_RATES,
    'question': "What is the interest rate for Medium risk?"
}, {
    'doc_file_path': './docs/Bank Loan Overall Risk Policy.pdf',
    'collection_name': constants.RAG_COLLECTION_LOAN_OVERALL_RISK_POLICY,
    'question': "What is the risk when credit score is 455 and account status is good-standing."
}]:

    data = load_pdf_file(file_path=rag["doc_file_path"])
    documents = text_split(data, chunk_size=200, chunk_overlap=50)

    vector_store = RAG(
        documents=documents,
        collection_name=rag["collection_name"],
        reload_collection=True
    )

    query_result = vector_store.query(
        rag['question'],
        top_k=2
    )
