from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

expenses = []


class ExpenseIn(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseIn):
    new_expense = {"id": len(expenses) + 1, **expense.model_dump()}
    expenses.append(new_expense)
    return new_expense


@app.get("/expenses")
def list_expenses():
    return expenses


@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")


@app.delete("/reset", status_code=204)
def reset():
    expenses.clear()