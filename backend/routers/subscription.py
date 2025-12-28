from fastapi import APIRouter, HTTPException
from models import TrialCodeRedeem
from services.subscription_service import (
    get_subscription,
    is_subscription_active,
    redeem_trial_code
)

router = APIRouter()

@router.get("/{telegram_id}/status")
async def subscription_status(telegram_id: int):
    try:
        subscription = await get_subscription(telegram_id)
        is_active = await is_subscription_active(telegram_id)
        return {
            "subscription": subscription,
            "is_active": is_active
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{telegram_id}/redeem")
async def redeem_code(telegram_id: int, code_data: TrialCodeRedeem):
    try:
        result = await redeem_trial_code(telegram_id, code_data.code)
        if result["success"]:
            return result
        raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
