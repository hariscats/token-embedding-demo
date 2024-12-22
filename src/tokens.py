from transformers import GPT2Tokenizer

def tokenize_text(text: str):
    """
    Tokenizes input text using GPT-2 tokenizer.
    """
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return tokenizer.tokenize(text)
