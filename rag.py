import os
from typing import List
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from util.log_util import print_message, print_documents

class RAG:
    """
    RAG(Retrieval-Augmented Generation) class built upon OpenAI and Milvus.
    """

    def __init__(
            self, 
            documents: List,
            collection_name: str, 
            db_name: str = "milvus", 
            reload_collection: bool = False,
            db_file_path: str = "./milvus.db",
            embedding_model: str = "text-embedding-3-large",
            metric_type: str = "IP"):

        self.embeddings_model = OpenAIEmbeddings(
            model=embedding_model, 
            dimensions=1024, 
            api_key=os.getenv('OPENAI_API_KEY'))

        connection_args = {"uri": db_file_path, "db_name": db_name}
        index_params = {"index_type": "FLAT", "metric_type": metric_type}

        if os.path.exists(db_file_path):

            self.vector_store = Milvus(
                auto_id=True,
                embedding_function=self.embeddings_model,
                collection_name=collection_name,
                connection_args=connection_args,
                index_params=index_params,
                consistency_level="Strong",
                drop_old=False
            )

            if reload_collection:
                print_message(f"Reloaded collection {collection_name} in existing vector store.")
                self.vector_store.drop()
                self.vector_store.add_documents(documents)

        else:
            print_message(f"Creating vector store with collection {collection_name}.")
            self.vector_store = Milvus.from_documents(
                auto_id=True,
                documents=documents,
                embedding=self.embeddings_model,
                collection_name=collection_name,
                connection_args=connection_args,
                index_params=index_params
            )

    def query(
        self,
        question: str,
        top_k: int = 2
    ):
        """
        Answer the given question with the retrieved knowledge.
        """
        documents = self.vector_store.similarity_search(question, k=top_k)
        print_documents(documents)
        result = "".join(document.page_content + "\n" for document in documents)
        print_message(result)
        return result
