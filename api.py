from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI
app = FastAPI(title="PITAP — Payment Failure Classification API", version="2.1.0")
# --- Enums ---
class Gateway(str, Enum):
    razorpay = "RazorpayV2"

# --- Models ---
class PaymentFailureRequest(BaseModel):
    txn_id: str = Field(..., description="Unique transaction identifier", json_schema_extra={"example": "TXN-20240115-001"})
    gateway: Gateway = Field(..., json_schema_extra={"example": "RazorpayV2"})
    amount: float = Field(..., gt=0, le=500000, description="Transaction amount in INR. Must be > 0", json_schema_extra={"example": 1250.00})
    error_code: str = Field(..., description="Raw error code from gateway", json_schema_extra={"example": "ERR_UPSTREAM_TIMEOUT"})
    retry_count: int = Field(0, ge=0, le=5, json_schema_extra={"example": 0})
    hour_of_day: int = Field(..., ge=0, le=23, json_schema_extra={"example": 14})

class BatchRequest(BaseModel):
    transactions: List[PaymentFailureRequest] = Field(
        ..., 
        max_length=100, 
        description="Max 100 transactions per batch"
    )
    customer_id: Optional[str] = Field(None, json_schema_extra={"example": "CUST-00012345"})
from fastapi import FastAPI, HTTPException, status

# 1. Initialize the FastAPI app
# (Ensure this is at the top of your file or right before the routes)
# app = FastAPI(title="PITAP — Payment Failure Classification API", version="2.1.0")

@app.post("/classify", status_code=status.HTTP_200_OK)
async def classify_single(req: PaymentFailureRequest):
    """
    Endpoint to classify a single payment failure.
    """
    # This is where your logic will eventually go
    return {"message": "Received", "txn_id": req.txn_id}

@app.post("/classify/batch")
async def classify_batch(batch: BatchRequest):
    """
    Endpoint to classify a batch of failures.
    """
    return {"message": f"Processed {len(batch.transactions)} transactions"}

@app.get("/health")
async def health():
    """
    System health check.
    """
    return {"status": "healthy", "version": "2.1.0"}
    
if __name__ == "__main__":
    print("Code loaded successfully!")
    
    # Simple test to check if Pydantic model initializes correctly
    test_data = {
        "txn_id": "TEST-123",
        "gateway": "RazorpayV2",
        "amount": 100.0,
        "error_code": "SUCCESS",
        "hour_of_day": 10
    }
    
    try:
        model = PaymentFailureRequest(**test_data)
        print("Pydantic model validated successfully:", model.txn_id)
    except Exception as e:
        print("Validation error:", e)