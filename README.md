# 💳 Personal Expense Tracker

A full-stack personal finance tracking application built with **FastAPI**, **Streamlit**, and **MySQL** - featuring a classy dark UI, real-time analytics, and monthly trend visualisation.

---

## 🖼️ Features

- **Add & Update Expenses** - Log multiple expenses per day across 6 categories
- **Daily Summary Cards** - Instant view of daily total, number of entries, and top category
- **Analytics Dashboard** - Breakdown by category with percentage distribution
- **Monthly Trends** - Line chart showing month-over-month spending
- **Quick Date Filters** - This Week, This Month, Last Month, Last 3 Months
- **Live API Status** - Sidebar indicator showing backend health
- **Dark Luxury UI** - Refined dark theme with gold accents

---

## 🗂️ Project Structure

```
expense-tracker/
├── backend/
│   ├── server.py          # FastAPI application & endpoints
│   ├── db_helper.py       # MySQL database layer with connection pooling
│   ├── logging_setup.py   # Rotating file + console logger
│   └── .env               # Database credentials (not committed)
├── frontend/
│   ├── app.py             # Main Streamlit app + global CSS theme
│   ├── add_update_ui.py   # Add/Update expenses tab
│   └── analytics_ui.py    # Analytics & charts tab
├── database.sql           # DB & table setup script
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up the database
```bash
mysql -u root -p < database.sql
```

### 4. Configure environment variables
Edit `backend/.env` with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=expense_manager
```

### 5. Run the backend
```bash
cd backend
uvicorn server:app --reload
```

### 6. Run the frontend (new terminal)
```bash
cd frontend
streamlit run app.py
```

Visit **http://localhost:8501** in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Backend health check |
| GET | `/expenses/{date}` | Fetch expenses for a date |
| POST | `/expenses/{date}` | Add/update expenses for a date |
| POST | `/analytics/` | Category breakdown for date range |
| GET | `/analytics/monthly` | Month-over-month trend data |
| POST | `/analytics/total` | Total spend for date range |

---

## 🏷️ Expense Categories

| Category | Icon |
|----------|------|
| Rent | 🏠 |
| Food | 🍔 |
| Shopping | 🛍️ |
| Entertainment | 🎬 |
| Utilities | ⚡ |
| Others | 📦 |

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, MySQL (with connection pooling)
- **Frontend**: Streamlit, Pandas
- **Database**: MySQL
- **Logging**: Python logging with rotating file handler

---

## ⚠️ Important Notes for Visitors

### Backend Wake-up Time
The backend is hosted on **Render's free tier** which sleeps after 15 minutes  of inactivity. If you see "API Offline" on first load, please wait 30-60 seconds and refresh the page. It will wake up automatically.

### Shared Database
This app uses a **shared database** for demo purposes, meaning all visitors see the same data. To avoid overwriting each other's entries, please test on different dates. A user login system is planned as a future enhancement.

### Database Availability
The database is hosted on **freesqldatabase.com** free tier which has a limited validity period. If the app stops working, the database may need to be renewed.

## Future Enhancements
- User authentication and login system (private data per user)
- Budget setting and alerts
- Export expenses to CSV or PDF
- Mobile-friendly UI

---

## Author
- Shijin Ramesh  
[LinkedIn](https://www.linkedin.com/in/shijinramesh/) | [Portfolio](https://www.shijinramesh.co.in/)
