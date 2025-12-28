from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from services.summary_service import get_period_summary, generate_csv_export
import io

router = APIRouter()

@router.get("/{telegram_id}/weekly")
async def weekly_summary(telegram_id: int):
    try:
        summary = await get_period_summary(telegram_id, days=7)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/monthly")
async def monthly_summary(telegram_id: int):
    try:
        summary = await get_period_summary(telegram_id, days=30)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/alltime")
async def alltime_summary(telegram_id: int):
    try:
        summary = await get_period_summary(telegram_id)
        return summary
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/export")
async def export_csv(telegram_id: int):
    try:
        csv_content = await generate_csv_export(telegram_id)
        if csv_content:
            return StreamingResponse(
                io.StringIO(csv_content),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=transactions.csv"}
            )
        raise HTTPException(status_code=404, detail="No data to export")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
