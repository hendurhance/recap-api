import re
from datetime import datetime
from fastapi import HTTPException, status

DATE_FORMAT = "%Y-%m-%d"


def validate_date(date_str):
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def validate(start_date, end_date):
    if start_date is None or not validate_date(start_date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid start date",
        )
    if end_date is None or not validate_date(end_date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid end date",
        )
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date should be less than end date",
        )
    if start_date > datetime.today().strftime(DATE_FORMAT) or end_date > datetime.today().strftime(DATE_FORMAT):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date and end date should be less than today's date",
        )
