# src/app.py
import os
from flask import Flask, request, render_template_string
from tokens import tokenize_text
from embeddings import get_sentence_embedding
from search import get_top_k_similar
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>LLM Tokens & Semantic Search Demo</title>
</head>
<body>
  <h1>LLM Tokens & Semantic Search Demo</h1>
  <form method="POST" action="/">
    <label for="query">Enter your text:</label><br>
    <input type="text" id="query" name="query" size="60"/><br><br>
    <input type="submit" value="Submit"/>
  </form>
  
  {% if tokens %}
    <h2>Tokenization (GPT-2)</h2>
    <p><strong>Tokens:</strong> {{ tokens }}</p>
    <p><strong>Number of tokens:</strong> {{ num_tokens }}</p>
  {% endif %}

  {% if results %}
    <h2>Semantic Search Results</h2>
    <ol>
      {% for item in results %}
      <li><strong>Passage:</strong> {{ item['text'] }}<br>
          <strong>Cosine Similarity:</strong> {{ item['score']|round(4) }}</li>
      {% endfor %}
    </ol>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    tokens = []
    results = []
    
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        # 1. Tokenize
        tokens = tokenize_text(query)
        # 2. Embed
        query_embedding = get_sentence_embedding(query)
        # 3. Semantic Search
        results = get_top_k_similar(query_embedding, k=3)

    return render_template_string(
        HTML_TEMPLATE,
        tokens=tokens,
        num_tokens=len(tokens),
        results=results
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
