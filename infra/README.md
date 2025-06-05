# Infrastructure

This directory contains the Bicep templates used to deploy the Azure Cost Optimizer.

## Deploying

Use the Azure CLI to deploy `main.bicep` to your subscription:

```bash
az deployment group create \
  --resource-group <resource-group> \
  --template-file main.bicep
```
