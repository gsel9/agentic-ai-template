# Implementing A Reference Agentic-AI Architecture

- https://github.com/microsoft/azure-genai-design-patterns/tree/main
- https://microsoft.github.io/multi-agent-reference-architecture/docs/reference-architecture/Reference-Architecture.html


## Setup
1. Create a resource group, Storage Account, AI Search, and a Foundry resource
2. Go to Storage Account > Data Storage > Containers:
    - Create a new data container
    - Create directories for PDF and JSON data and upload files
3. Go to Foundry portal
    - Deploy embedding model (e.g., ada)
    - Deploy chat model (e.g., gpt-4o)
4. Go to AI Search > Import Data (new)
    - Select Azure Blob Storage
    - RAG
    - Complete schema with API key as authentication 
    - Debug resource access: Verify that API access is enabled in Settings > Keys, 
5. Test the indexer in Search Management > Indexes > RAG-{id}
6. Create a Cosmos DB
    - Select Cosmos DB for NoSQL
    - Complete schema
    - Create a container for conversation history in Data Explorer
    - Debug RU/s limit: 
        - Go to Settings > Account Throughput
        - Select custom amount and assign value 
7. Create an App Services
    - Select Web App
    - Enable deploymnet via GitHub
8. Configure App Services
    - Settings > Configuration > Stack settings: Add `bash startup.sh` to startup command text field
        - The startup script should include `gunicorn -k uvicorn.workers.UvicornWorker main:app`
    - Settings > Env variables: Create variables based on .env file (makes env variables reachable in code via `os.getenv({})`)
9. From code repo, pull to download the the actions workflow file 
10. Push code to main/master to trigger the deployment process

### Add Agent

Create new Foundry resource (not AI hub). 

**Security**
Using API keys is an alternative to configuring IAM permissions for resources. E.g., the Storage accoutn would need to be configured with Storage Blob Data Contributor role to Azure AI Search. However, in case entra ID/Active Directory does not work, rely on API authentication and Key Vault.


## Test

To test locally, run:
```
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
In the browser, go to: http://127.0.0.1:8000/docs

---

To test programatically by querying Azure, copy the default domina UR from the Wep App overview page (NOTE: add prefix https://). Create a sample JSON payload, e.g.:
```
{'item_id': '000', 'user_id': 'user-007', 'conv_id': '000', 'user_input': 'Hello!'}
```
Run the query in Python
```
import requests
requests.post(url, json=json).json()
```
