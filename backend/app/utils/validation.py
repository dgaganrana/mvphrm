from fastapi import HTTPException, status
from pydantic import EmailStr

def validate_email(email: str) -> EmailStr:
    try:
        return EmailStr.validate(email)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

def validate_status(status: str) -> str:
    if status not in ["Present", "Absent"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be either 'Present' or 'Absent'"
        )
    return status
