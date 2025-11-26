import agent

def test_loren(output: str):
    required_keywords = ["medium", "4.885%", "455", "good-standing"]
    for keyword in required_keywords:
        assert keyword.lower() in output.lower(), f"Result does not contain '{keyword}' (case-insensitive)"

def test_matt(output: str):
    required_keywords = ["medium", "4.885%", "685", "closed"]
    for keyword in required_keywords:
        assert keyword.lower() in output.lower(), f"Result does not contain '{keyword}' (case-insensitive)"

def test_andy(output: str):
    required_keywords = ["low", "3.175%", "840", "closed"]
    for keyword in required_keywords:
        assert keyword.lower() in output.lower(), f"Result does not contain '{keyword}' (case-insensitive)"

for test_case in [{
    'query': 'Customer Information: Loren, 1111, loren@gmail.com',
    'test_func': test_loren
}, {
    'query': 'Customer Information: Matt, 2222, matt@yahoo.com',
    'test_func': test_matt
}, {
    'query': 'Customer Information: Andy, 4444, matt@yahoo.com'
}]:
    
    response = agent.run_agent(test_case['query'], '123456')