# LLM Tokens & Semantic Search Demo

This project demonstrates:
1. **Tokenization** with GPT-2.
2. **Embeddings** using Sentence Transformers.
3. **Semantic search** in a text corpus.

---

## Project Structure

```
token-embedding-demo/
├── README.md                
├── requirements.txt         
├── src/
│   ├── app.py               
│   ├── tokens.py            
│   ├── embeddings.py        
│   ├── search.py            
│   └── data/
│       └── corpus.txt       
└── infra/
    └── main.bicep           
```

---

## Installation (Local)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/token-embedding-demo.git
   cd token-embedding-demo
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare embeddings**:
   ```bash
   python src/search.py
   ```

5. **Run the app**:
   ```bash
   python src/app.py
   ```

6. **Open in browser**: `http://127.0.0.1:5050/`

---

## Using the App

1. Enter a query (e.g., "To be or not to be").
2. See:
   - **Tokenization**: Tokens + token count.
   - **Semantic Search**: Top-3 most similar corpus matches.

---

## Optional: Azure Deployment

1. **Deploy Infrastructure**:
   ```bash
   az group create -n MyResourceGroup -l eastus
   az deployment group create \
       --resource-group MyResourceGroup \
       --template-file infra/main.bicep \
       --parameters appServicePlanName="llmDemoPlan" webAppName="llmDemoWebApp"
   ```

2. **Deploy Code**:
   ```bash
   zip -r app.zip .
   az webapp deployment source config-zip \
       --resource-group MyResourceGroup \
       --name llmDemoWebApp \
       --src app.zip
   ```

3. **Access App**:
   ```bash
   az webapp show --resource-group MyResourceGroup --name llmDemoWebApp --query "defaultHostName" -o tsv
   ```

---

## Notes

- Update `src/data/corpus.txt` to customize the text corpus.
- Re-run `python src/search.py` to regenerate embeddings after updates.

---

## Technical Details

- **Tokenization**: Uses GPT-2 tokenizer.
- **Embeddings**: Generated via `sentence-transformers/all-MiniLM-L6-v2`.
- **Semantic Search**: Cosine similarity over query and corpus embeddings.
