# app/schemas/solve.py
from pydantic import BaseModel
from typing import Optional, List

class SolveRequest(BaseModel):
    prompt: str
    credentials: dict
    files: Optional[List] = None

class Customer(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Invoice(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    due_date: Optional[str] = None

class ParsedTask(BaseModel):
    task_type: str
    customer: Optional[Customer] = None
    invoice: Optional[Invoice] = None

class PlanStep(BaseModel):
    action: str
    args: dict