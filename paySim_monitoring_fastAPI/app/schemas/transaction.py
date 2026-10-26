from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal 
from typing import Literal

class TransactionEvent(BaseModel):
    event_type: Literal["payment.created"]
    transaction_id: str
    merchant_id: str
    customer_id: str
    amount: Decimal = Field(gt=0)
    currency: str
    status: Literal["SUCCESS", "FAILED", "PENDING"]
    created_at: datetime