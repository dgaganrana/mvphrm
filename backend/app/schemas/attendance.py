from pydantic import BaseModel, field_validator, field_serializer, ConfigDict
from typing import Literal
from datetime import date

class AttendanceBase(BaseModel):
    employee_id: int
    date: date | str  # Accept both date objects and ISO date strings
    status: Literal["Present", "Absent"]
    
    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        """Convert string dates to date objects"""
        if isinstance(v, str):
            try:
                from datetime import datetime
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v

class AttendanceCreate(AttendanceBase):
    pass

class Attendance(AttendanceBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_serializer('date')
    def serialize_date(self, value: date) -> str:
        """Serialize date to ISO format string"""
        if isinstance(value, date):
            return value.isoformat()
        return str(value)




