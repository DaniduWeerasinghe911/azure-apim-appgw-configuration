# Resource analysis using Azure Resource Graph
import os
from azure.identity import ClientSecretCredential
from azure.mgmt.resourcegraph import ResourceGraphClient

def find_idle_vms():
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
    client = ResourceGraphClient(credential)
    query = """
    Resources
    | where type == 'microsoft.compute/virtualmachines'
    | where properties.extended.instanceView.powerState.code == 'PowerState/deallocated'
    | project name, id, location
    """
    result = client.resources(
        query=query,
        subscriptions=[subscription_id],
    )
    return result.data["rows"]

def find_unattached_disks():
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
    client = ResourceGraphClient(credential)
    query = """
    Resources
    | where type == 'microsoft.compute/disks'
    | where properties.diskState == 'Unattached'
    | project name, id, location
    """
    result = client.resources(
        query=query,
        subscriptions=[subscription_id],
    )
    return result.data["rows"]
