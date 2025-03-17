from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from api.utils import get_current_user
from api.supabase_client import supabase

router = APIRouter()

def calculate_sector_allocation(investments: List[Dict[str, any]]) -> List[Dict]:
    sector_totals = {}
    stock_contributions = {}
    total_investment = 0

    fund_ids = [inv['fund_id'] for inv in investments]

    # Fetch all sector allocations
    sector_resp = supabase.from_("sector_allocations").select("fund_id, sector, percentage").in_("fund_id", fund_ids).execute()
    sector_allocations = sector_resp.data or []

    # Fetch all stock allocations
    stocks_resp = supabase.from_("stock_allocations").select("fund_id, stock, percentage").in_("fund_id", fund_ids).execute()
    stock_allocations = stocks_resp.data or []

    # Ensure all sectors are included even if no investment is found
    all_sectors = {alloc['sector'] for alloc in sector_allocations}

    for investment in investments:
        investment_amount = investment['amount']
        fund_id = investment['fund_id']

        # Get all sector allocations for this fund
        relevant_sectors = [alloc for alloc in sector_allocations if alloc['fund_id'] == fund_id]

        for sector_alloc in relevant_sectors:
            sector = sector_alloc['sector']
            sector_percentage = sector_alloc['percentage']
            sector_amount = (sector_percentage / 100) * investment_amount

            # Track total amount per sector
            sector_totals[sector] = sector_totals.get(sector, 0) + sector_amount
            total_investment += sector_amount

            # Track stock contributions
            relevant_stocks = [stock for stock in stock_allocations if stock['fund_id'] == fund_id]
            for stock_alloc in relevant_stocks:
                stock = stock_alloc['stock']
                stock_percentage = stock_alloc['percentage']
                stock_amount = (stock_percentage / 100) * sector_amount

                stock_contributions.setdefault(sector, {})
                stock_contributions[sector][stock] = stock_contributions[sector].get(stock, 0) + stock_amount

    # Ensure all sectors appear in the result
    result = []
    for sector in all_sectors:
        amount = sector_totals.get(sector, 0)
        sector_percentage = (amount / total_investment) * 100 if total_investment > 0 else 0

        stocks = [
            {
                "stock": stock,
                "amount": round(stock_amount, 2),
                "percentage": round((stock_amount / amount) * 100, 2) if amount > 0 else 0
            }
            for stock, stock_amount in stock_contributions.get(sector, {}).items()
        ]

        result.append({
            "sector": sector,
            "amount": round(amount, 2),
            "percentage": round(sector_percentage, 2),
            "stocks": sorted(stocks, key=lambda x: x['percentage'], reverse=True)
        })

    return sorted(result, key=lambda x: x['percentage'], reverse=True)

@router.get("/sector-allocation")
def get_sector_allocation(user_id: str = Depends(get_current_user)):
    try:
        investments_resp = supabase.from_("investments").select("fund_id, amount").eq("user_id", user_id).execute()
        investments = investments_resp.data or []

        if not investments:
            return {"status": "error", "message": "No investments found for this user."}

        allocation_data = calculate_sector_allocation(investments)
        return {"status": "success", "data": allocation_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching sector allocations.")
