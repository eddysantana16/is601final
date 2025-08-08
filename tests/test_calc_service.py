from app.routes.calculations import perform_operation
import pytest

def test_add(): assert perform_operation("add", 2, 3) == 5
def test_subtract(): assert perform_operation("subtract", 7, 2) == 5
def test_multiply(): assert perform_operation("multiply", 3, 4) == 12
def test_divide_ok(): assert perform_operation("divide", 8, 2) == 4
def test_divide_by_zero():
    with pytest.raises(Exception):
        perform_operation("divide", 1, 0)
def test_power(): assert perform_operation("power", 2, 3) == 8
def test_invalid_operation():
    with pytest.raises(Exception):
        perform_operation("nope", 1, 1)
