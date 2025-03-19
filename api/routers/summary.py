from fastapi import APIRouter, Depends, HTTPException, Query
from api.supabase_client import supabase
from api.utils import get_current_user
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/performance-summary")
def get_performance_summary(
    user_id: str = Depends(get_current_user),
    period: str = Query("1m", description="Time period for data: 1m, 3m, 6m, 1y, 2y, or max")
):
    try:
        # Fetch user investments from Supabase
        response = supabase.table("investments").select("*").eq("user_id", user_id).execute()
        investments = response.data

        if not investments:
            raise HTTPException(status_code=404, detail="No investments found for this user.")

        # Determine the date range based on the period selected
        end_date = datetime.utcnow()
        earliest_investment_date = min(datetime.fromisoformat(inv["purchase_date"]) for inv in investments)

        if period != "max":
            days_map = {"1m": 30, "3m": 90, "6m": 180, "1y": 365, "2y": 730}
            start_date = max(earliest_investment_date, end_date - timedelta(days=days_map.get(period, 30)))
        else:
            start_date = earliest_investment_date

        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        performance_data = []
        total_investment = 0

        for date in date_range:
            total_value = 0

            for inv in investments:
                purchase_date = datetime.fromisoformat(inv["purchase_date"])

                if date >= purchase_date:  # Investment should be counted only after purchase
                    initial_value = inv["amount"]
                    final_value = inv["amount"] * (1 + inv["returns_since_investment"] / 100)

                    # Compute linear interpolation only for the period after the purchase
                    days_held = (end_date - purchase_date).days or 1
                    elapsed_days = (date - purchase_date).days
                    growth_factor = elapsed_days / days_held

                    linear_value = initial_value + (final_value - initial_value) * max(growth_factor, 0)
                    total_value += linear_value

            performance_data.append({"date": date.strftime('%Y-%m-%d'), "value": round(total_value, 2)})

        # Compute final statistics
        total_investment = sum(inv["amount"] for inv in investments)
        current_value = performance_data[-1]["value"] if performance_data else 0
        total_returns = current_value - total_investment
        total_percentage = (total_returns / total_investment) * 100 if total_investment else 0

        return {
            "status": "success",
            "total_value": round(current_value, 2),
            "total_returns": round(total_returns, 2),
            "percentage_change": round(total_percentage, 2),
            "data": performance_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
