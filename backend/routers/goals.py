from fastapi import APIRouter, HTTPException
from models import GoalCreate, Goal
from services.goals_service import (
    create_goal,
    get_active_goals,
    get_completed_goals,
    update_goal_progress
)
from typing import List

router = APIRouter()

@router.post("/{telegram_id}", response_model=Goal)
async def add_goal(telegram_id: int, goal: GoalCreate):
    try:
        result = await create_goal(
            telegram_id,
            goal.goal_name,
            goal.target_amount,
            goal.deadline,
            goal.auto_save_percent
        )
        if result:
            return result
        raise HTTPException(status_code=400, detail="Failed to create goal")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/active", response_model=List[Goal])
async def list_active_goals(telegram_id: int):
    try:
        goals = await get_active_goals(telegram_id)
        return goals
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{telegram_id}/completed", response_model=List[Goal])
async def list_completed_goals(telegram_id: int):
    try:
        goals = await get_completed_goals(telegram_id)
        return goals
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
