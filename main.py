from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

expenses = []
next_id = 1


class ExpenseIn(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseIn):
    global next_id
    new_expense = {"id": next_id, **expense.model_dump()}
    next_id += 1
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


@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseIn):
    for i, existing in enumerate(expenses):
        if existing["id"] == expense_id:
            updated = {"id": expense_id, **expense.model_dump()}
            expenses[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Expense not found")


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    for i, existing in enumerate(expenses):
        if existing["id"] == expense_id:
            expenses.pop(i)
            return
    raise HTTPException(status_code=404, detail="Expense not found")


@app.delete("/reset", status_code=204)
def reset():
    global next_id
    expenses.clear()
    next_id = 1