import os

def print_documents(documents: list):
    
    if not os.getenv('DEBUG', 'False').lower() == 'true':
        return
    
    print("\n========== Documents ==========")
    for idx, document in enumerate(documents):
        print(f">>> doc {idx} <<<")
        print(document.metadata)
        print(document.page_content)

def print_message(message: str):
    
    if not os.getenv('DEBUG', 'False').lower() == 'true':
        return
    
    print("\n========== Message ==========")
    print("{message}".format(message=message))