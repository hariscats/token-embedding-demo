import torch
from transformers import AutoTokenizer, AutoModel

def get_sentence_embedding(text: str):
    """
    Generates a sentence-level embedding using a pretrained model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings[0].numpy()
