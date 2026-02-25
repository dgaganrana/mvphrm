from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.attendance import Attendance as AttendanceModel
from app.models.employee import Employee as EmployeeModel
from app.schemas.attendance import AttendanceCreate, Attendance


class AttendanceService:
    """Service layer for attendance business logic"""

    @staticmethod
    async def _employee_exists(db: AsyncSession, employee_id: int) -> bool:
        """Check if an employee exists"""
        result = await db.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def mark_attendance(db: AsyncSession, record_data: AttendanceCreate) -> Attendance:
        """Create an attendance record"""
        # Validate employee exists
        if not await AttendanceService._employee_exists(db, record_data.employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        new_record = AttendanceModel(
            employee_id=record_data.employee_id,
            date=record_data.date,
            status=record_data.status,
        )
        db.add(new_record)
        try:
            await db.commit()
            await db.refresh(new_record)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance record already exists for this employee on this date."
            )
        return new_record

    @staticmethod
    async def get_attendance(db: AsyncSession, employee_id: int) -> list[Attendance]:
        """Get all attendance records for an employee"""
        # Validate employee exists
        if not await AttendanceService._employee_exists(db, employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        result = await db.execute(
            select(AttendanceModel).where(AttendanceModel.employee_id == employee_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_attendance_by_date(db: AsyncSession, employee_id: int, date: str) -> Attendance:
        """Get attendance record for a specific employee on a specific date"""
        # Validate employee exists
        if not await AttendanceService._employee_exists(db, employee_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        result = await db.execute(
            select(AttendanceModel).where(
                (AttendanceModel.employee_id == employee_id) & 
                (AttendanceModel.date == date)
            )
        )
        record = result.scalar_one_or_none()
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No attendance record found for this employee on the specified date"
            )
        return record

    @staticmethod
    async def get_all_attendance(db: AsyncSession) -> list[Attendance]:
        """Get all attendance records across all employees"""
        result = await db.execute(select(AttendanceModel))
        return result.scalars().all()
