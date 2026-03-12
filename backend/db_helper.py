import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from logging_setup import setup_logger
import os
from pathlib import Path

try:
    import streamlit as st
    DB_HOST = st.secrets["DB_HOST"]
    DB_USER = st.secrets["DB_USER"]
    DB_PASSWORD = st.secrets["DB_PASSWORD"]
    DB_NAME = st.secrets["DB_NAME"]
    DB_PORT = int(st.secrets["DB_PORT"])
except Exception:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(__file__).parent / ".env")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
    DB_NAME = os.getenv("DB_NAME", "expense_manager")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))

connection_pool = pooling.MySQLConnectionPool(
    pool_name="expense_pool",
    pool_size=5,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)


@contextmanager
def get_db_cursor(commit=False):
    connection = None
    cursor = None
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor(dictionary=True)
        yield cursor
        if commit:
            connection.commit()
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        if connection and commit:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        return cursor.fetchall()


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total 
               FROM expenses WHERE expense_date
               BETWEEN %s AND %s  
               GROUP BY category;''',
            (start_date, end_date)
        )
        return cursor.fetchall()


def fetch_monthly_summary():
    logger.info("fetch_monthly_summary called")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT 
                DATE_FORMAT(expense_date, '%Y-%m') as month,
                SUM(amount) as total
               FROM expenses
               GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
               ORDER BY month ASC;'''
        )
        return cursor.fetchall()


def fetch_total_expenses(start_date, end_date):
    logger.info(f"fetch_total_expenses called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT SUM(amount) as total FROM expenses WHERE expense_date BETWEEN %s AND %s",
            (start_date, end_date)
        )
        result = cursor.fetchone()
        return result['total'] if result['total'] else 0.0


if __name__ == "__main__":
    expenses = fetch_expenses_for_date("2024-09-30")
    print(expenses)
    summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    for record in summary:
        print(record)