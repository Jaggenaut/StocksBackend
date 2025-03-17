from fastapi import APIRouter, Depends, HTTPException, Query
from api.utils import get_current_user
from api.supabase_client import supabase
from datetime import datetime, timedelta

router = APIRouter()

def calculate_irr(investment: dict, current_date: datetime) -> float:
    try:
        days_held = (current_date - datetime.fromisoformat(investment['purchase_date'])).days
        annual_return = investment['returns_since_investment']
        return investment['amount'] * (1 + annual_return) ** (days_held / 365)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating IRR: {str(e)}")

def get_start_date(period: str, end_date: datetime) -> datetime:
    try:
        if period == "1m":
            return end_date - timedelta(days=30)
        elif period == "3m":
            return end_date - timedelta(days=90)
        elif period == "6m":
            return end_date - timedelta(days=180)
        elif period == "1y":
            return end_date - timedelta(days=365)
        elif period == "2y":
            return end_date - timedelta(days=730)
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error determining start date: {str(e)}")

@router.get("/performance-summary")
def get_performance_summary(
    user_id: str = Depends(get_current_user),
    period: str = Query("1m", description="Time period for data: 1m, 3m, 6m, 1y, 2y, or max")
):
    try:
        response = supabase.table("investments").select("*").eq("user_id", user_id).execute()
        investments = response.data

        if not investments:
            raise HTTPException(status_code=404, detail="No investments found for this user.")

        end_date = datetime.utcnow()
        start_date = get_start_date(period, end_date)

        if start_date is None:
            start_date = min(datetime.fromisoformat(inv['purchase_date']) for inv in investments)

        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        performance_data = []
        for date in date_range:
            total_value = sum(calculate_irr(inv, date) for inv in investments)
            performance_data.append({"date": date.strftime('%Y-%m-%d'), "value": round(total_value, 2)})

        total_investment = sum(inv['amount'] for inv in investments)
        current_value = performance_data[-1]['value'] if performance_data else 0
        total_returns = current_value - total_investment
        total_percentage = (total_returns / total_investment) * 100 if total_investment else 0

        return {
            "status": "success",
            "total_value": current_value,
            "total_returns": total_returns,
            "percentage_change": round(total_percentage, 2),
            "data": performance_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
