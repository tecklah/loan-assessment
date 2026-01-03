# Loan Assessment Application

## Description
An AI-powered loan assessment application that uses LangGraph agents, RAG (Retrieval-Augmented Generation), and SQL database tools to assist with loan application assessments. The application provides intelligent responses by querying both structured database data and unstructured document knowledge bases.

## Tech Stack
- **Framework**: Streamlit (Interactive web UI)
- **AI/ML**: 
  - LangChain & LangGraph (Agent orchestration)
  - OpenAI GPT-4.1 (Language model)
  - OpenAI Embeddings (text-embedding-3-large)
- **Vector Database**: Milvus Lite (Document embeddings storage)
- **Relational Database**: PostgreSQL (Structured loan data)
- **Document Processing**: PDFPlumber, PyPDF (PDF parsing)
- **Language**: Python 3.x

## Features
- Interactive chat interface for loan assessment queries
- SQL database querying via LangChain toolkit
- RAG-based document retrieval from PDF knowledge base
- Session management for conversational context
- Multi-tool AI agent with database and document search capabilities

## Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- OpenAI API key
- PDF documents for knowledge base (stored in `docs/` folder)

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd loan-assessment
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
DB_USERNAME=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_NAME=loanassessment
```

### 5. Set up the PostgreSQL database
Create the database and tables using the provided SQL script:
```bash
psql -U your_username -d loanassessment -f db.sql
```

### 6. Prepare knowledge base documents
Place your PDF documents in the `docs/` folder. These will be indexed by the RAG system.

## Starting the Application

### Run the Streamlit app
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

### Alternative: Using the run script
```bash
chmod +x run.sh
./run.sh
```

## Project Structure
```
loan-assessment/
├── app.py                 # Streamlit web application
├── agent.py              # LangGraph agent implementation
├── rag.py                # RAG system with Milvus
├── load_rag.py           # RAG data loader
├── prompts.py            # System prompts for agents
├── constants.py          # Application constants
├── requirements.txt      # Python dependencies
├── db.sql               # Database schema
├── docs/                # PDF knowledge base documents
├── util/                # Utility modules
│   ├── doc_util.py      # Document processing utilities
│   └── log_util.py      # Logging utilities
├── test_agent.py        # Agent tests
├── test_rag.py          # RAG tests
└── README.md            # This file
```

## Usage
1. Start the application using `streamlit run app.py`
2. Enter your loan assessment queries in the chat input
3. The AI agent will:
   - Query the PostgreSQL database for structured loan data
   - Search the document knowledge base using RAG
   - Provide comprehensive responses based on both sources
4. Use the "New Session" button in the sidebar to start a fresh conversation

## Testing
Run the test files to verify functionality:
```bash
# Test RAG system
python test_rag.py

# Test agent system
python test_agent.py
```

## Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4.1 | `sk-...` |
| `DB_USERNAME` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `your_password` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_NAME` | Database name | `loanassessment` |

## Troubleshooting
- **Database connection errors**: Verify PostgreSQL is running and credentials in `.env` are correct
- **OpenAI API errors**: Check your API key is valid and has sufficient credits
- **Vector store issues**: Delete `milvus.db` and restart to rebuild the vector index
- **PDF parsing errors**: Ensure PDF documents are valid and not password-protected