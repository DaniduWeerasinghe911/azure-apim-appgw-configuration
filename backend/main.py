from fastapi import FastAPI, HTTPException

from .cost import get_subscription_costs

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Azure Cost Optimizer API"}


@app.get("/costs")
def read_costs():
    """Retrieve basic cost information for the subscription."""
    try:
        return get_subscription_costs()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
