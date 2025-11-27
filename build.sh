#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the package to install
PACKAGE_NAME="load_dotenv langchain langgraph langchain_community langchain_text_splitters langchain_openai langchain-milvus pymilvus pymilvus[model] pymilvus[milvus_lite] pypdf streamlit mysqldb psycopg2 pdfplumber"

echo "Attempting to install $PACKAGE_NAME..."

# Check if pip is available
if ! command -v pip &> /dev/null
then
    echo "pip could not be found. Please ensure Python and pip are installed and in your PATH."
    exit 1
fi

# Install the package
pip install "$PACKAGE_NAME"

echo "$PACKAGE_NAME installed successfully."