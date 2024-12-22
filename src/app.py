# src/app.py
"""
Flask-based LLM tokens & semantic search demonstration.

This module sets up a Flask application that:
1. Receives user input (query text).
2. Tokenizes the text using a GPT-2 tokenizer.
3. Generates an embedding using a sentence-transformer model.
4. Performs a semantic search to find the top-K most similar corpus lines.
"""

import logging
import os
from flask import Flask, request, render_template_string

# Local module imports
from tokens import tokenize_text
from embeddings import get_sentence_embedding
from search import get_top_k_similar

app = Flask(__name__)

# Set up basic logging for the application
logging.basicConfig(level=logging.INFO)

#: HTML template for our simple demo page
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
    <label for="query">Enter your text:</label><br />
    <input type="text" id="query" name="query" size="60" /><br /><br />
    <input type="submit" value="Submit" />
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
      <li>
        <strong>Passage:</strong> {{ item['text'] }}<br />
        <strong>Cosine Similarity:</strong> {{ item['score']|round(4) }}
      </li>
      {% endfor %}
    </ol>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Displays a form to capture user input, and upon submission:
      1. Tokenizes the user query (GPT-2).
      2. Generates embeddings for the query.
      3. Retrieves top-3 semantically similar lines from the corpus.
    
    Returns:
        (str): Rendered HTML with tokenization info and search results.
    """
    tokens = []
    results = []

    if request.method == "POST":
        # Retrieve the user query from the form
        query = request.form.get("query", "").strip()
        app.logger.info("Received query: '%s'", query)

        # 1. Tokenize
        tokens = tokenize_text(query)
        app.logger.debug("Tokens: %s", tokens)

        # 2. Embed
        query_embedding = get_sentence_embedding(query)
        app.logger.debug("Query embedding shape: %s", query_embedding.shape)

        # 3. Semantic Search
        results = get_top_k_similar(query_embedding, k=3)
        app.logger.info("Found %d results for the query.", len(results))

    return render_template_string(
        HTML_TEMPLATE,
        tokens=tokens,
        num_tokens=len(tokens),
        results=results
    )


def run_dev_server():
    """
    Runs the Flask development server on 0.0.0.0:5000.
    
    This function can be called directly for local testing
    or triggered by your environment when deploying.
    """
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    run_dev_server()
