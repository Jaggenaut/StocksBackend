# Mutual Fund Dashboard Backend

This is the backend API for the Mutual Fund Dashboard project, developed using **FastAPI** and **Supabase** as the database. It provides multiple endpoints for investment management, performance analysis, stock overlap, and sector allocation.

## 🚀 Features

- **User Authentication** with JWT.
- **Investment Management**: Retrieve investments for a user.
- **Stock Overlap Analysis**: Identify overlapping stocks across mutual funds.
- **Sector Allocation Summary**: Detailed allocation of investments across sectors and stocks.
- **Performance Summary**: Track investment performance over various time periods.

## 📂 Project Structure

```
├── api
│   ├── __init__.py
│   ├── supabase_client.py   # Supabase client setup
│   ├── utils.py             # Utility functions including authentication
│   ├── routers
│   │   ├── investments.py   # Investment retrieval endpoint
│   │   ├── overlap.py       # Stock overlap endpoint
│   │   ├── sector.py        # Sector allocation endpoint
│   │   └── performance.py   # Performance summary endpoint
├── main.py                  # FastAPI app instance
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mutual-fund-backend
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file to store environment variables:

```env
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<your-supabase-api-key>
JWT_SECRET=<your-jwt-secret>
```

### 5. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## 🔄 API Endpoints

### **Authentication**

- Endpoint: `/auth/login`
- Description: Logs in a user and returns a JWT token.

### **Get Investments**

- Endpoint: `/investment`
- Method: `GET`
- Description: Fetches the list of investments for the current user.

### **Stock Overlap**

- Endpoint: `/overlap`
- Method: `GET`
- Description: Retrieves overlapping stocks across funds for the user.

### **Sector Allocation**

- Endpoint: `/sector-allocation`
- Method: `GET`
- Description: Provides a breakdown of investment allocation by sector.

### **Performance Summary**

- Endpoint: `/performance-summary`
- Method: `GET`
- Query Params: `period` (e.g., `1m`, `3m`, `6m`, `1y`, `2y`, `max`)
- Description: Returns investment performance data over the specified period.

## 🔐 Authentication

All endpoints require a valid JWT token. Pass the token in the `Authorization` header:

```bash
Authorization: Bearer <your-jwt-token>
```
