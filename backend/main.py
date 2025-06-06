import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
from fastapi import FastAPI, HTTPException, Depends
from auth import AzureADBearer
from resource_analysis import find_idle_vms, find_unattached_disks
from cost import get_subscription_costs
from openai_service import generate_insight_summary

app = FastAPI()

azure_ad_scheme = AzureADBearer()

@app.get("/")
def read_root(token=Depends(azure_ad_scheme)):
    return {"message": "Azure Cost Optimizer API"}

@app.get("/costs")
def read_costs(token=Depends(azure_ad_scheme)):
    """Retrieve basic cost information for the subscription."""
    try:
        return get_subscription_costs()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/idle-vms")
def get_idle_vms(token=Depends(azure_ad_scheme)):
    """Retrieve a list of idle virtual machines."""
    try:
        return {"idle_vms": find_idle_vms()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/unattached-disks")
def get_unattached_disks(token=Depends(azure_ad_scheme)):
    """Retrieve a list of unattached disks."""
    try:
        return {"unattached_disks": find_unattached_disks()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/insight-summary")
def insight_summary(data: dict, token=Depends(azure_ad_scheme)):
    try:
        summary = generate_insight_summary(data)
        return {"summary": summary}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
