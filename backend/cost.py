import os
from datetime import date

from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient


def get_subscription_costs():
    """Return cost data for the configured subscription."""
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

    if not all([tenant_id, client_id, client_secret, subscription_id]):
        raise ValueError("Azure credentials are not fully configured")

    credential = ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )
    cost_client = CostManagementClient(credential)

    today = date.today()
    start = today.replace(day=1)

    query = {
        "type": "ActualCost",
        "timeframe": "Custom",
        "timePeriod": {"from": start.isoformat(), "to": today.isoformat()},
        "dataset": {
            "granularity": "Daily",
            "aggregation": {
                "totalCost": {"name": "PreTaxCost", "function": "Sum"}
            },
        },
    }

    result = cost_client.query.usage(
        scope=f"/subscriptions/{subscription_id}", parameters=query
    )
    return result.as_dict()
