"""Common dependencies for API endpoints"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.services.employee_service import EmployeeService
from app.services.attendance_service import AttendanceService


# These are commonly used dependencies that can be injected into endpoint functions
# Example usage: async def my_endpoint(employee_service: EmployeeService = Depends(get_employee_service))

async def get_employee_service() -> EmployeeService:
    """Get the employee service instance"""
    return EmployeeService()


async def get_attendance_service() -> AttendanceService:
    """Get the attendance service instance"""
    return AttendanceService()
