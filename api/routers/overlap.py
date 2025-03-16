from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from utils import get_current_user
from api.supabase_client import supabase

router = APIRouter()

@router.get("/overlap")
def get_stock_overlap(user_id: str = Depends(get_current_user)):
    # Get funds the user has invested in
    investments_resp = supabase.from_("investments").select("fund_id").eq("user_id", user_id).execute()
    investments = investments_resp.data

    if not investments:
        raise HTTPException(status_code=404, detail="No investments found for the user")

    fund_ids = [inv['fund_id'] for inv in investments]

    # Fetch stock allocations for these funds
    allocations_resp = supabase.from_("stock_allocations").select("fund_id, stock, percentage").in_("fund_id", fund_ids).execute()
    stock_allocations = allocations_resp.data

    # Fetch mutual fund names
    funds_resp = supabase.from_("mutual_funds").select("id, name").in_("id", fund_ids).execute()
    funds = {fund['id']: fund['name'] for fund in funds_resp.data}

    # Prepare overlap data
    overlap_data: Dict[str, List[Dict[str, Any]]] = {}

    for allocation in stock_allocations:
        fund_name = funds.get(allocation['fund_id'], "Unknown Fund")
        if fund_name not in overlap_data:
            overlap_data[fund_name] = []
        overlap_data[fund_name].append({
            "stock": allocation['stock'],
            "allocation_percentage": allocation['percentage']
        })

    # Create unique nodes for funds and stocks
    fund_nodes = list(overlap_data.keys())
    stock_nodes = list({stock['stock'] for stocks in overlap_data.values() for stock in stocks})
    all_nodes = fund_nodes + stock_nodes

    # Map node names to indices
    name_to_index = {name: idx for idx, name in enumerate(all_nodes)}

    # Create nodes array
    nodes = [{"name": name} for name in all_nodes]

    # Create links based on overlap and allocation percentage
    links = []
    for fund, stocks in overlap_data.items():
        for stock_data in stocks:
            links.append({
                "source": name_to_index[fund],
                "target": name_to_index[stock_data["stock"]],
                "value": stock_data["allocation_percentage"]
            })

    return {"nodes": nodes, "links": links}