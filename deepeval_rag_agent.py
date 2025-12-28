import os
import constants
from dotenv import load_dotenv
from util.doc_util import load_pdf_file, text_split
from langchain_openai import ChatOpenAI
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.synthesizer import Synthesizer
from deepeval.dataset import EvaluationDataset
from deepeval.models import GPTModel
from rag import RAG
from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)
from deepeval.metrics import GEval
from deepeval import evaluate

load_dotenv()

# Create evaluation model using gpt-4o-mini
eval_model = GPTModel(model="gpt-4o-mini")

relevancy = ContextualRelevancyMetric(model=eval_model)
recall = ContextualRecallMetric(model=eval_model)
precision = ContextualPrecisionMetric(model=eval_model)

answer_correctness = GEval(
    name="Answer Correctness",
    criteria="Evaluate if the actual output's 'answer' property is correct and complete from the input and retrieved context. If the answer is not correct or complete, reduce score.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
    model=eval_model
)

citation_accuracy = GEval(
    name="Citation Accuracy",
    criteria="Check if the citations in the actual output are correct and relevant based on input and retrieved context. If they're not correct, reduce score.",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
    model=eval_model
)

llm = ChatOpenAI(
    openai_api_base="https://api.openai.com/v1",
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model_name="gpt-4o-mini",
    temperature=0.1,
    max_tokens=1000,
)

# Load and split documents
data = load_pdf_file(file_path=constants.FILE_INTEREST_RATE_POLICY)
documents = text_split(data, chunk_size=200, chunk_overlap=50)

# Extract contexts from documents - each context should be a list
contexts = [[doc.page_content] for doc in documents]

print(f"Number of document chunks: {len(contexts)}")

# Generate goldens from contexts using gpt-4o-mini
synthesizer = Synthesizer(model="gpt-4o-mini")
goldens = synthesizer.generate_goldens_from_contexts(
    contexts=contexts,
    max_goldens_per_context=2
)

dataset = EvaluationDataset(goldens=goldens)

print(f"Number of goldens generated: {len(dataset.goldens)}")

# Create RAG agent
agent = RAG(llm, documents, constants.RAG_COLLECTION_LOAN_INTEREST_RATES)

# Generate test cases
test_cases = []
for golden in dataset.goldens:
    retrieved_docs = agent.retrieve(golden.input)
    response = agent.query(golden.input)
    test_case = LLMTestCase(
        input=golden.input,
        actual_output=str(response),
        retrieval_context=retrieved_docs,
        expected_output=golden.expected_output
    )
    test_cases.append(test_case)

print(f"Number of test cases: {len(test_cases)}")

retriever_metrics = [relevancy, recall, precision]

evaluate(test_cases, retriever_metrics)

generator_metrics = [answer_correctness, citation_accuracy]

evaluate(test_cases, generator_metrics)