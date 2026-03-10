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
    - Settings > Configuration > Stack settings: Add `bash startup.sh` to Startup command text field
    - Settings > Env variables: Create variables based on .env file (makes env variables reachable in code via `os.getenv({})`)


## Test

To test locally, run:
```
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
In the browser, go to: http://127.0.0.1:8000/docs

To start the API after deployment, include in the startup bash script:
`gunicorn -k uvicorn.workers.UvicornWorker main:app`.


# Parking lot


- From AI Search > Settings > Keys, verify that API access is enabled
- In Foundry, deploy an embedding model (eg, ada) and a chat model (eg, gtp-4o)
- In storage account, create data container, one sub-directory with json data, and one directory with pdf data 
- Cosmos: Data explorer, new container
    - 


- From storage accoutn, set IAM for AI Search:
    - managed identity of your Azure AI Search service
    - Storage Blob Data Contributor
    - 
- In Storage Account, create a data container with sub-directories for json and pdf data

TODO: 
- Programatically upload data to storage container
- Deploy embedding model and chat model 
- Run azure indexer 
- Create a http-triggered function to upload data (pdf/json) into Blob storage

If entra ID/Active Directory does not work, rely on API authentication.

## Configure App Service

2. Create an App Services resource
3. In App Services, create a Web App
    - Runtime stack: Python 3.11
    - Continuous deployment: Enable (add gitHub details)
  - Creating the Web App with link to GitHub will add Action workflows that must be pulled into the app dev repo
5. Push the app code to git, triggering deployment process
  - Follow the deployment process under the repo's Actions/ tab
6. In the Azure portal, from the service menu on the left, choose Settings > Configuration > Stack Settings
7. Add `bash startup.sh` as Startup command and click refresh
8. Go to overview page and click restart app
9. Monitor application start-up process in the left service menu under Log Stream

Debug: 
- Refresh Configuration > Stack settings and restart App in overview page
- Tick "always on" in Configuration > General settings to avoid app timeouts

The code in `startup.sh` should be 
```
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
```
