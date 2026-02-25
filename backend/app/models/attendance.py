from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.db import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)  # Date object
    status = Column(String, nullable=False)  # "Present" or "Absent"

    employee = relationship("Employee", backref="attendance_records")

    __table_args__ = (
        UniqueConstraint("employee_id", "date", name="unique_employee_date"),
    )
