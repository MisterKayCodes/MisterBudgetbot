from fastapi import APIRouter, HTTPException
from services.advisor_service import (
    analyze_spending_habits,
    analyze_savings_habits,
    generate_recommendations
)

router = APIRouter()

@router.get("/{telegram_id}/spending")
async def spending_analysis(telegram_id: int):
    try:
        analysis = await analyze_spending_habits(telegram_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/savings")
async def savings_analysis(telegram_id: int):
    try:
        analysis = await analyze_savings_habits(telegram_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/recommendations")
async def get_recommendations(telegram_id: int):
    try:
        recommendations = await generate_recommendations(telegram_id)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
