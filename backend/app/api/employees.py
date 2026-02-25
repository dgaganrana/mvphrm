from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.employee import Employee, EmployeeCreate
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new employee"""
    return await EmployeeService.create_employee(db, employee)


@router.get("/", response_model=list[Employee])
async def list_employees(db: AsyncSession = Depends(get_db)):
    """Get all employees"""
    return await EmployeeService.get_employees(db)


@router.get("/{id}", response_model=Employee)
async def get_employee(id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific employee by ID"""
    return await EmployeeService.get_employee(db, id)


@router.put("/{id}", response_model=Employee)
async def update_employee(id: int, employee: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    """Update an employee"""
    return await EmployeeService.update_employee(db, id, employee)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(id: int, db: AsyncSession = Depends(get_db)):
    """Delete an employee"""
    await EmployeeService.delete_employee(db, id)
    return None
