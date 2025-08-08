# app/routes/calculations.py
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.routes.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["Calculations"])

def perform_operation(operation: str, a: float, b: Optional[float]) -> float:
    if operation == "add": return a + (b or 0)
    if operation == "subtract": return a - (b or 0)
    if operation == "multiply": return a * (b if b is not None else 1)
    if operation == "divide":
        if b == 0: raise HTTPException(status_code=400, detail="Division by zero is not allowed")
        return a / (b if b is not None else 1)
    if operation == "power": return a ** (b if b is not None else 1)
    raise HTTPException(status_code=400, detail="Invalid operation")

@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create_calculation(
    payload: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = perform_operation(payload.operation, payload.operand1, payload.operand2)
    row = models.Calculation(
        user_id=current_user.id,
        operation=payload.operation,
        operand1=payload.operand1,
        operand2=payload.operand2,
        result=result,
    )
    db.add(row); db.commit(); db.refresh(row)
    return row

@router.get("/", response_model=List[schemas.CalculationRead])
def list_calculations(
    op: Optional[str] = Query(default=None, description="Filter by operation"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    q = db.query(models.Calculation).filter(models.Calculation.user_id == current_user.id)
    if op: q = q.filter(models.Calculation.operation == op)
    return q.order_by(models.Calculation.created_at.desc()).offset(offset).limit(limit).all()

@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def get_calculation(calc_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    row = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not row: raise HTTPException(status_code=404, detail="Calculation not found")
    return row

@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update_calculation(calc_id: int, payload: schemas.CalculationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    row = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not row: raise HTTPException(status_code=404, detail="Calculation not found")
    row.operation = payload.operation
    row.operand1 = payload.operand1
    row.operand2 = payload.operand2
    row.result = perform_operation(payload.operation, payload.operand1, payload.operand2)
    db.commit(); db.refresh(row)
    return row

@router.delete("/{calc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(calc_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    row = db.query(models.Calculation).filter(models.Calculation.id == calc_id, models.Calculation.user_id == current_user.id).first()
    if not row: raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(row); db.commit()
    return

@router.get("/reports/summary", response_model=schemas.ReportSummary)
def get_summary_report(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    rows = db.query(
        models.Calculation.operation, models.Calculation.operand1, models.Calculation.operand2, models.Calculation.result
    ).filter(models.Calculation.user_id == current_user.id).all()
    if not rows:
        return {"total_calculations": 0, "by_operation": {}, "avg_operand1": None, "avg_operand2": None, "avg_result": None, "most_used_operation": None}
    from collections import Counter
    from statistics import mean
    ops = [r[0] for r in rows]; counts = Counter(ops); most_used = max(counts, key=counts.get)
    def _avg(ix: int):
        vals = [float(r[ix]) for r in rows if r[ix] is not None]
        return round(mean(vals), 2) if vals else None
    return {
        "total_calculations": len(rows),
        "by_operation": dict(counts),
        "avg_operand1": _avg(1),
        "avg_operand2": _avg(2),
        "avg_result": _avg(3),
        "most_used_operation": most_used,
    }
