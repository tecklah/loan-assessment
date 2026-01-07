from deepeval.metrics import (
    GEval,
    TaskCompletionMetric,
    AnswerRelevancyMetric
)
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval import evaluate
from dotenv import load_dotenv
import agent

# Load environment variables first
load_dotenv(dotenv_path='.env')

answer_relevancy = AnswerRelevancyMetric(threshold=0.8, model="gpt-4o-mini")
# task_completion_metric = TaskCompletionMetric(model="gpt-4o-mini")

# Custom accuracy metric
accuracy_metric = GEval(
    name="Loan Assessment Accuracy",
    criteria="The output correctly identifies the customer, retrieves accurate credit score, calculates appropriate risk level, and provides the correct interest rate",
    evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    threshold=0.8,
    model="gpt-4o-mini"
)

# Create test cases list to collect all evaluations
test_cases = []

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="What is the loan assessment for Loren, 1111?",
            expected_output="Medium risk with 4.885% interest rate for Loren (account 1111, credit score 455, good-standing, Singaporean)"
        ),
        # Golden(
        #     input="Customer Information: Matt, 2222",
        #     expected_output="Recommend the loan interest rate, although not Singaporean but got a PR. (account 2222, credit score 685, closed, Non-Singaporean)"
        # ),
        # Golden(
        #     input="Customer Information: Andy, 4444",
        #     expected_output="Not recommend although risk is low, because Non- Singaporean and PR status is false. (account 4444, credit score 840, good-standing, Non-Singaporean)"
        # ),
        # Golden(
        #     input="What is the loan assessment for Hilda, 3333?",
        #     expected_output="Medium risk with 4.885% interest rate for Hilda (account 3333, credit score 825, delinquent, Singaporean)"
        # ),
        # Golden(
        #     input="What is the loan assessment for Kit, 5555?",
        #     expected_output="High risk with 6.325% interest rate for Kit (account 5555, credit score 350, delinquent, Singaporean)"
        # )
    ]
)

# Build test cases from dataset
for golden in dataset.goldens:
    # Run agent and get response
    response = agent.run_agent(golden.input, "test_session")
    
    # Create test case
    test_case = LLMTestCase(
        input=golden.input,
        actual_output=response,
        expected_output=golden.expected_output
    )
    
    test_cases.append(test_case)

# NOW EVALUATE - this was missing!
evaluate(test_cases, metrics=[accuracy_metric, answer_relevancy])