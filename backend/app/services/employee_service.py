from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.employee import Employee as EmployeeModel
from app.schemas.employee import EmployeeCreate, Employee


class EmployeeService:
    """Service layer for employee business logic"""

    @staticmethod
    async def create_employee(db: AsyncSession, employee_data: EmployeeCreate) -> Employee:
        """Create a new employee"""
        new_employee = EmployeeModel(
            name=employee_data.name,
            email=employee_data.email,
            department=employee_data.department,
        )
        db.add(new_employee)
        try:
            await db.commit()
            await db.refresh(new_employee)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this email already exists or invalid data."
            )
        return new_employee

    @staticmethod
    async def get_employee(db: AsyncSession, employee_id: int) -> Employee:
        """Get a single employee by ID"""
        result = await db.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        return employee

    @staticmethod
    async def get_employees(db: AsyncSession) -> list[Employee]:
        """Get all employees"""
        result = await db.execute(select(EmployeeModel))
        return result.scalars().all()

    @staticmethod
    async def update_employee(db: AsyncSession, employee_id: int, employee_data: EmployeeCreate) -> Employee:
        """Update an existing employee"""
        result = await db.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        employee.name = employee_data.name
        employee.email = employee_data.email
        employee.department = employee_data.department

        try:
            await db.commit()
            await db.refresh(employee)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use or invalid data."
            )
        return employee

    @staticmethod
    async def delete_employee(db: AsyncSession, employee_id: int) -> None:
        """Delete an employee"""
        result = await db.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        employee = result.scalar_one_or_none()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )
        await db.delete(employee)
        await db.commit()
