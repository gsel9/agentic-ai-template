# Implementing A Reference Agentic-AI Architecture

- https://github.com/microsoft/azure-genai-design-patterns/tree/main
- https://microsoft.github.io/multi-agent-reference-architecture/docs/reference-architecture/Reference-Architecture.html

## Resource setup
1. Create a resource group, AI Search, Storage Account, Cosmos DB, Foundry resource 
- From AI Search > Settings > Keys, verify that API access is enabled
- In Foundry, deploy an embedding model (eg, ada) and a chat model (eg, gtp-4o)
- In storage account, create data container, one sub-directory with json data, and one directory with pdf data 
- Cosmos: Data explorer, new container
    - Debug RU/s limit: Settings > Accoutn Throughput


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
