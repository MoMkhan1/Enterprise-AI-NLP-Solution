"""
Chatbot LLM Module (distilgpt2)
--------------------------------
Interactive financial assistant using Hugging Face Transformers.
"""

import logging
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os  # <-- for creating logs folder

# -----------------------------
# Ensure Logs Folder Exists
# -----------------------------
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_FILE = os.path.join(LOGS_DIR, "chatbot_history.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Load Model and Tokenizer
# -----------------------------
MODEL_NAME = "distilgpt2"
logger.info(f"Loading chatbot model: {MODEL_NAME}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Ensure pad token is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# -----------------------------
# Chatbot Pipeline
# -----------------------------
chatbot_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1,  # CPU
    framework="pt"
)

# -----------------------------
# Function: Generate Response
# -----------------------------
def get_response(user_input: str) -> str:
    """
    Generate response from chatbot using distilgpt2.
    Explicitly sets truncation and max_new_tokens to avoid warnings.
    """
    logger.info(f"User: {user_input}")
    
    output = chatbot_pipeline(
        user_input,
        max_new_tokens=150,   # limit output length
        truncation=True,      # explicitly truncate input if too long
        pad_token_id=tokenizer.eos_token_id
    )
    
    response = output[0]['generated_text'][len(user_input):].strip()
    logger.info(f"Bot: {response}")
    return response

# -----------------------------
# Interactive Mode
# -----------------------------
if __name__ == "__main__":
    print("🤖 Chatbot is running... (type 'exit' to quit)")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting chatbot.")
            break
        bot_response = get_response(user_input)
        print(f"{bot_response}")
