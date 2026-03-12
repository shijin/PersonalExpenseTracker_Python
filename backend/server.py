from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel, validator

app = FastAPI(
    title="Expense Tracker API",
    description="Personal Expense Tracking System API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Expense(BaseModel):
    amount: float
    category: str
    notes: str

    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @validator('category')
    def category_must_be_valid(cls, v):
        valid = ["Rent", "Food", "Shopping", "Entertainment", "Utilities", "Others"]
        if v not in valid:
            raise ValueError(f'Category must be one of {valid}')
        return v


class DateRange(BaseModel):
    start_date: date
    end_date: date

    @validator('end_date')
    def end_date_must_be_after_start(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Expense Tracker API is running"}


@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    try:
        expenses = db_helper.fetch_expenses_for_date(expense_date)
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve expenses: {str(e)}")


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    try:
        db_helper.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
        return {"message": "Expenses updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update expenses: {str(e)}")


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    try:
        data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
        if not data:
            return {}
        total = sum(row['total'] for row in data)
        breakdown = {}
        for row in data:
            percentage = (row['total'] / total) * 100 if total != 0 else 0
            breakdown[row['category']] = {
                "total": row['total'],
                "percentage": percentage
            }
        return breakdown
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve analytics: {str(e)}")


@app.get("/analytics/monthly")
def get_monthly_trends():
    try:
        data = db_helper.fetch_monthly_summary()
        if not data:
            return []
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve monthly trends: {str(e)}")


@app.post("/analytics/total")
def get_total(date_range: DateRange):
    try:
        total = db_helper.fetch_total_expenses(date_range.start_date, date_range.end_date)
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve total: {str(e)}")