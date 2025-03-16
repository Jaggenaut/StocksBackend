from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from utils import get_current_user
from supabase_client import supabase

router = APIRouter()

def calculate_sector_allocation(investments: List[Dict[str, any]]) -> List[Dict]:
    sector_totals = {}
    total_investment = 0

    fund_ids = [inv['fund_id'] for inv in investments]

    # Fetch sector allocations for these funds
    allocations_resp = supabase.from_("sector_allocations").select("fund_id, sector, percentage").in_("fund_id", fund_ids).execute()
    sector_allocations = allocations_resp.data

    for investment in investments:
        investment_amount = investment['amount']
        relevant_allocations = [alloc for alloc in sector_allocations if alloc['fund_id'] == investment['fund_id']]

        for allocation in relevant_allocations:
            amount = (allocation['percentage'] / 100) * investment_amount
            sector_totals[allocation['sector']] = sector_totals.get(allocation['sector'], 0) + amount
            total_investment += amount

    result = []
    for sector, amount in sector_totals.items():
        percentage = (amount / total_investment) * 100 if total_investment > 0 else 0
        result.append({
            "sector": sector,
            "amount": round(amount, 2),
            "percentage": round(percentage, 2)
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
