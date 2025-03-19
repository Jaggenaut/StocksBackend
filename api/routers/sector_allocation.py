from fastapi import APIRouter, Depends, HTTPException
from api.supabase_client import supabase
from api.utils import get_current_user
from collections import defaultdict

router = APIRouter()

@router.get("/sector-allocation")
def investment_breakdown(user_id: str = Depends(get_current_user)):
    try:
        # Fetch all user investments
        response = (
            supabase.table("investments")
            .select("fund_id, amount")
            .eq("user_id", user_id)
            .execute()
        )
        investments = response.data
        if not investments:
            raise HTTPException(status_code=404, detail="No investments found for this user.")
        
        # Fetch sector allocations with sector names
        sector_response = (
            supabase.table("sector_allocations")
            .select("fund_id, sector_id, sectors(name), percentage")
            .execute()
        )
        sector_allocations = sector_response.data
        
        # Fetch stock allocations with stock names
        stock_response = (
            supabase.table("stock_allocations")
            .select("fund_id, stock_id, stocks(name), percentage")
            .execute()
        )
        stock_allocations = stock_response.data
        
        # Fetch sector-stock mappings
        sector_stocks_response = (
            supabase.table("sector_stocks")
            .select("sector_id, stock_id")
            .execute()
        )
        sector_stocks = sector_stocks_response.data
        
        # Calculate total investment
        total_investment = sum(inv["amount"] for inv in investments)
        
        # Calculate sector-wise investment
        sector_investments = defaultdict(lambda: {"total_investment": 0, "investment_percentage": 0, "stocks": defaultdict(lambda: {"amount": 0, "percentage": 0})})
        
        for inv in investments:
            fund_id = inv["fund_id"]
            fund_amount = inv["amount"]
            
            # Allocate amount into sectors
            for sector in sector_allocations:
                if sector["fund_id"] == fund_id:
                    sector_id = sector["sector_id"]
                    sector_name = sector["sectors"]["name"]
                    sector_percentage = sector["percentage"] / 100
                    sector_amount = fund_amount * sector_percentage
                    sector_investments[sector_name]["total_investment"] += sector_amount
                    
                    # Allocate amount into stocks within that sector
                    for stock in stock_allocations:
                        if stock["fund_id"] == fund_id:
                            stock_id = stock["stock_id"]
                            stock_name = stock["stocks"]["name"]
                            stock_percentage = stock["percentage"] / 100
                            stock_amount = fund_amount * stock_percentage
                            
                            # Ensure the stock belongs to the sector
                            if any(s["sector_id"] == sector_id and s["stock_id"] == stock_id for s in sector_stocks):
                                sector_investments[sector_name]["stocks"][stock_name]["amount"] += stock_amount
        
        # Calculate percentages
        for sector_name, data in sector_investments.items():
            data["investment_percentage"] = round((data["total_investment"] / total_investment) * 100, 2) if total_investment else 0
            total_sector_investment = data["total_investment"]
            for stock_name, stock_data in data["stocks"].items():
                stock_data["percentage"] = round((stock_data["amount"] / total_sector_investment) * 100, 2) if total_sector_investment else 0
                stock_data["amount"] = round(stock_data["amount"], 2)
        
        # Convert defaultdict to normal dict
        result = {
            sector_name: {
                "total_investment": round(data["total_investment"], 2),
                "investment_percentage": data["investment_percentage"],
                "stocks": {stock_name: {"amount": stock_data["amount"], "percentage": stock_data["percentage"]} for stock_name, stock_data in data["stocks"].items()}
            }
            for sector_name, data in sector_investments.items()
        }
        
        return {"status": "success", "data": result}
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")