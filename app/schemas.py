from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Optional


# --------------------
# User Schemas
# --------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# --------------------
# Calculation Schemas
# --------------------
class CalculationBase(BaseModel):
    operation: str
    operand1: float
    operand2: Optional[float] = None
    result: float


class CalculationCreate(BaseModel):
    operation: str
    operand1: float
    operand2: Optional[float] = None


class CalculationRead(CalculationBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --------------------
# Reporting Schema
# --------------------
class ReportSummary(BaseModel):
    total_calculations: int
    by_operation: Dict[str, int]
    avg_operand1: Optional[float] = None
    avg_operand2: Optional[float] = None
    avg_result: Optional[float] = None
    most_used_operation: Optional[str] = None

class ReportSummary(BaseModel):
    total_calculations: int
    by_operation: Dict[str, int]
    avg_operand1: Optional[float] = None
    avg_operand2: Optional[float] = None
    avg_result: Optional[float] = None
    most_used_operation: Optional[str] = None
