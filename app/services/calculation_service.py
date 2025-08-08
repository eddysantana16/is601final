from collections import Counter
from typing import Optional, List, Dict
from statistics import mean


def perform_calculation(operation: str, operand1: float, operand2: Optional[float] = None) -> float:
    """Perform a basic calculation based on the operation."""
    if operation == "add":
        return operand1 + (operand2 or 0)
    elif operation == "sub":
        return operand1 - (operand2 or 0)
    elif operation == "mul":
        return operand1 * (operand2 or 1)
    elif operation == "div":
        if operand2 == 0:
            raise ValueError("Division by zero")
        return operand1 / (operand2 or 1)
    elif operation == "exp":
        return operand1 ** (operand2 or 1)
    elif operation == "mod":
        if operand2 == 0:
            raise ValueError("Modulo by zero")
        return operand1 % (operand2 or 1)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def generate_report(calculations: List[dict]) -> Dict:
    """
    Generate usage statistics from a list of calculations.
    Each calculation dict should have keys: operation, operand1, operand2, result.
    """
    total = len(calculations)
    if total == 0:
        return {
            "total_calculations": 0,
            "by_operation": {},
            "avg_operand1": None,
            "avg_operand2": None,
            "avg_result": None,
            "most_used_operation": None,
        }

    ops = [c["operation"] for c in calculations]
    op_counts = Counter(ops)
    most_used_op = max(op_counts, key=op_counts.get)

    return {
        "total_calculations": total,
        "by_operation": dict(op_counts),
        "avg_operand1": round(mean(c["operand1"] for c in calculations), 2),
        "avg_operand2": round(mean(c["operand2"] for c in calculations if c["operand2"] is not None), 2)
        if any(c["operand2"] is not None for c in calculations) else None,
        "avg_result": round(mean(c["result"] for c in calculations), 2),
        "most_used_operation": most_used_op,
    }
