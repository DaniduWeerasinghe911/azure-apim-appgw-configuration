# Azure Cost Optimizer

This project contains an initial scaffold for the **Azure Cost Optimizer** service. The goal is to build a small SaaS solution that analyzes Azure usage and highlights potential savings.

## Project Structure

- `frontend/` – React application (Vite) for the dashboard
- `backend/` – FastAPI server providing cost analysis APIs
- `infra/` – Bicep templates used to deploy the service

## Getting Started

1. Clone the repository
2. Install dependencies for the backend and frontend
   - `pip install fastapi uvicorn azure-identity azure-mgmt-costmanagement`
3. Set the following environment variables so the backend can query Azure Cost Management APIs:
   - `AZURE_TENANT_ID`
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_SUBSCRIPTION_ID`
4. Run the FastAPI server and start the React dev server

This repository is only a starting point. Follow the project plan to implement Azure authentication, cost data collection, the insights engine, and the web dashboard.

### API Endpoints

- `GET /` – Health check returning a welcome message
- `GET /costs` – Fetches basic cost data for the configured subscription

## Deploying Infrastructure

Run the following command with the Azure CLI to deploy the base resources defined in `infra/main.bicep`:

```bash
az deployment group create \
  --resource-group <resource-group> \
  --template-file infra/main.bicep
```
