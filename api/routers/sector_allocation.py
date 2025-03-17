from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from api.utils import get_current_user
from api.supabase_client import supabase

router = APIRouter()

def calculate_sector_allocation(investments: List[Dict[str, any]]) -> List[Dict]:
    sector_totals = {}
    stock_contributions = {}
    total_investment = 0

    fund_ids = [inv['fund_id'] for inv in investments]

    # Fetch sector allocations
    sector_resp = supabase.from_("sector_allocations").select("fund_id, sector, percentage").in_("fund_id", fund_ids).execute()
    sector_allocations = sector_resp.data

    # Fetch stock allocations
    stocks_resp = supabase.from_("stock_allocations").select("fund_id, stock, percentage").in_("fund_id", fund_ids).execute()
    stock_allocations = stocks_resp.data

    # Mapping from fund_id to sector
    fund_sector_map = {
        alloc['fund_id']: alloc['sector'] for alloc in sector_allocations
    }

    for investment in investments:
        investment_amount = investment['amount']
        fund_id = investment['fund_id']
        
        # Get sector and sector percentage for this fund
        sector_alloc = next((alloc for alloc in sector_allocations if alloc['fund_id'] == fund_id), None)
        if not sector_alloc:
            continue

        sector = sector_alloc['sector']
        sector_percentage = sector_alloc['percentage']
        sector_amount = (sector_percentage / 100) * investment_amount
        
        sector_totals[sector] = sector_totals.get(sector, 0) + sector_amount
        total_investment += sector_amount

        # Calculate stock contributions within this sector
        relevant_stocks = [stock for stock in stock_allocations if stock['fund_id'] == fund_id]
        for stock_alloc in relevant_stocks:
            stock = stock_alloc['stock']
            stock_percentage = stock_alloc['percentage']
            stock_amount = (stock_percentage / 100) * sector_amount
            
            stock_contributions.setdefault(sector, {})
            stock_contributions[sector][stock] = stock_contributions[sector].get(stock, 0) + stock_amount

    # Prepare final response
    result = []
    for sector, amount in sector_totals.items():
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
    investments_resp = supabase.from_("investments").select("fund_id, amount").eq("user_id", user_id).execute()
    investments = investments_resp.data

    if not investments:
        raise HTTPException(status_code=404, detail="No investments found for this user.")

    allocation_data = calculate_sector_allocation(investments)
    return allocation_data
