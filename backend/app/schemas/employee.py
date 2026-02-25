from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
