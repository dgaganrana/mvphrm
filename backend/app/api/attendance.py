from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.attendance import Attendance, AttendanceCreate
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=Attendance, status_code=status.HTTP_201_CREATED)
async def mark_attendance(record: AttendanceCreate, db: AsyncSession = Depends(get_db)):
    """Mark attendance for an employee"""
    return await AttendanceService.mark_attendance(db, record)


@router.get("/", response_model=list[Attendance])
async def get_all_attendance(db: AsyncSession = Depends(get_db)):
    """Get all attendance records"""
    return await AttendanceService.get_all_attendance(db)


@router.get("/{employee_id}", response_model=list[Attendance])
async def get_attendance(employee_id: int, db: AsyncSession = Depends(get_db)):
    """Get all attendance records for a specific employee"""
    return await AttendanceService.get_attendance(db, employee_id)


@router.get("/{employee_id}/{date}", response_model=Attendance)
async def get_attendance_by_date(employee_id: int, date: str, db: AsyncSession = Depends(get_db)):
    """Get attendance record for a specific employee on a specific date"""
    return await AttendanceService.get_attendance_by_date(db, employee_id, date)
