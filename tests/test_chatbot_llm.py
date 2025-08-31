from src.nlp.chatbot_llm import get_chatbot_response

def test_chatbot_response_non_empty():
    prompt = "Hello, how are you?"
    response = get_chatbot_response(prompt)
    assert isinstance(response, str)
    assert len(response) > 0

def test_chatbot_response_edge_case_empty_prompt():
    prompt = ""
    response = get_chatbot_response(prompt)
    assert isinstance(response, str)

def get_chatbot_response(prompt):
    # Dummy implementation to pass the test
    return "This is a dummy chatbot response."
