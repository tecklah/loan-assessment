from langchain_openai import ChatOpenAI
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, ContextualPrecisionMetric, FaithfulnessMetric, ContextualRelevancyMetric, ContextualRecallMetric
from deepeval import evaluate
from dotenv import load_dotenv
import os
import sys
from rag import RAG
import constants

# Load environment variables first
load_dotenv(dotenv_path='.env')

answer_relevancy = AnswerRelevancyMetric(threshold=0.8, model="gpt-4o-mini")
contextual_precision = ContextualPrecisionMetric(threshold=0.8, model="gpt-4o-mini")
contextual_relevancy = ContextualRelevancyMetric(threshold=0.4, model="gpt-4o-mini")
contextual_recall = ContextualRecallMetric(threshold=0.8, model="gpt-4o-mini")
faithfulness = FaithfulnessMetric(threshold=0.8, model="gpt-4o-mini")
llm = ChatOpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv('OPENAI_API_KEY'),
    model="gpt-4o-mini",
    temperature=0.1,
    max_tokens=1000,
)

interest_rate_test_cases = [
    LLMTestCase(
        input='What is the interest rate for low risk?',
        expected_output=(
            'The interest rate is 3.175%.'
        )
    ),
    LLMTestCase(
        input='What is the interest rate for medium risk?',
        expected_output=(
            'The interest rate is 4.885%.'
        )
    ),
]

overall_risk_test_cases = [
    LLMTestCase(
        input='What is the risk level for credit score 500 and account is closed.',
        expected_output=(
            'The risk level is high.'
        )
    ),
    LLMTestCase(
        input='What is the risk level for credit score 500 and account is good-standing.',
        expected_output=(
            'The risk level is medium.'
        )
    )
]

def test_rag_interest_rate():

    rag = RAG(
        llm, 
        None, 
        constants.RAG_COLLECTION_LOAN_INTEREST_RATES,
        reload_collection=False, 
        db_file_path="./milvus.db")

    for test_case in interest_rate_test_cases:

        actual_output, retrieved_contexts = rag.query(test_case.input)

        test_case.actual_output = actual_output
        test_case.retrieval_context = retrieved_contexts

    evaluate(interest_rate_test_cases, metrics=[answer_relevancy, contextual_precision, faithfulness, contextual_relevancy, contextual_recall])

def test_rag_overall_risk():

    rag = RAG(
        llm, 
        None, 
        constants.RAG_COLLECTION_LOAN_OVERALL_RISK_POLICY,
        reload_collection=False, 
        db_file_path="./milvus.db")

    for test_case in overall_risk_test_cases:

        actual_output, retrieved_contexts = rag.query(test_case.input, top_k=2)

        test_case.actual_output = actual_output
        test_case.retrieval_context = retrieved_contexts

    evaluate(overall_risk_test_cases, metrics=[answer_relevancy, contextual_precision, faithfulness, contextual_relevancy, contextual_recall])

if __name__ == "__main__":
    test_rag_interest_rate()
    test_rag_overall_risk()
    sys.exit(0)



