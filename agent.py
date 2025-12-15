import os
import constants
import prompts
from uuid import uuid4
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from util.doc_util import load_pdf_file, text_split
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import tool
from rag import RAG

load_dotenv()

chat_model = ChatOpenAI(
    openai_api_base="https://api.openai.com/v1",
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    model_name="gpt-4.1",
    temperature=0.1,
    max_tokens=1000,
)

db = SQLDatabase.from_uri("postgresql+psycopg2://" + os.getenv('DB_USERNAME') + ":" + os.getenv('DB_PASSWORD') + "@" + os.getenv('DB_HOST') + "/loanassessment")
toolkit = SQLDatabaseToolkit(db=db, llm=chat_model)
tools = toolkit.get_tools()

@tool(description="A tool to query the SQL database. Pass in a query/prompt that you want to run against the database.")
def check_database(query: str) -> str:
    # print("check_database query:", query)
    """
    A tool to query the SQL database.
    """
    system_prompt = prompts.DATABASE_PROMPT.format(
        dialect=db.dialect,
        top_k=1,
    )

    db_agent = create_agent(
        chat_model,
        tools,
        system_prompt=system_prompt
    )
    
    content = None
    for step in db_agent.stream(
        {'messages': [AIMessage(query)]},
        stream_mode="values"
    ):
        step["messages"][-1].pretty_print()
        content = step["messages"][-1].content

    return content

reload_collection = False
data = None
documents = None

if not os.path.exists(constants.RAG_VECTOR_STORE_PATH) or reload_collection:
    data = load_pdf_file(file_path=constants.FILE_OVERALL_RISK_POLICY)
    documents = text_split(data, chunk_size=200, chunk_overlap=50)

vector_store_loan_overall_risk_policy = RAG(documents, constants.RAG_COLLECTION_LOAN_OVERALL_RISK_POLICY, reload_collection=reload_collection)

if not os.path.exists(constants.RAG_VECTOR_STORE_PATH) or reload_collection:
    data = load_pdf_file(file_path=constants.FILE_INTEREST_RATE_POLICY)
    documents = text_split(data, chunk_size=200, chunk_overlap=50)

vector_store_loan_interest_rate_policy = RAG(documents, constants.RAG_COLLECTION_LOAN_INTEREST_RATES, reload_collection=reload_collection)

@tool(description="A tool to check the overall risk policy for a loan application using RAG.")
def check_overall_risk(query: str):
    return vector_store_loan_overall_risk_policy.query(query)

@tool(description="A tool to check the interest rate for a loan application using RAG.")
def check_interest_rate(query: str):
    return vector_store_loan_interest_rate_policy.query(query)

supervisor_agent = create_agent(
    chat_model,
    tools=[check_database, check_overall_risk, check_interest_rate],
    system_prompt=prompts.SUPERVISOR_PROMPT,
    checkpointer=InMemorySaver(),
)

def run_agent(query: str, session_id: str) -> str:
    last_message = None
    config = {
        'configurable': {
            'thread_id': session_id
        }
    }   
    for step in supervisor_agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        {**config, "stream_mode": "values"}
    ):
        for update in step.values():
            for message in update.get("messages", []):
                last_message = message
                message.pretty_print()

    return last_message.content

if __name__ == "__main__":

    query = "Customer Information: Loren, 1111, loren@gmail.com"
    # query = "Customer Information: Matt, 2222, matt@yahoo.com"
    # query = "Customer Information: Andy, 4444, matt@yahoo.com"

    run_agent(query, str(uuid4()))
