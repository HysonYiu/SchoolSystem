import os
from datetime import date, timedelta

CYCLE_START = os.getenv("CYCLE_START_DATE", "2025-09-02")
CYCLE_LENGTH = 7

TIMETABLE = {
    1: [
        ("08:20","09:00","ICT","Rm51"),
        ("09:00","09:40","ICT","Rm51"),
        ("10:00","10:40","MATH","Rm41"),
        ("10:40","11:20","ENG","Rm41"),
        ("11:30","12:10","M2","Rm41"),
        ("12:10","12:50","CHI","Rm41"),
        ("14:00","14:40","CHEM","Rm41"),
        ("14:40","15:20","CHEM","Rm41"),
    ],
    2: [
        ("08:20","09:00","ENG","Rm41"),
        ("09:00","09:40","M2","Rm41"),
        ("10:00","10:40","MATH","Rm41"),
        ("10:40","11:20","MATH","Rm41"),
        ("11:30","12:10","ICT","Rm51"),
        ("12:10","12:50","ICT","Rm51"),
        ("14:00","14:40","OLE","Rm41"),
        ("14:40","15:20","OLE","Rm41"),
    ],
    3: [
        ("08:20","09:00","MATH","Rm41"),
        ("09:00","09:40","ENG","Rm41"),
        ("10:00","10:40","CHI","Rm41"),
        ("10:40","11:20","CHI","Rm41"),
        ("11:30","12:10","ICT","Rm51"),
        ("12:10","12:50","ICT","Rm51"),
        ("14:00","14:40","CHEM","Rm36"),
        ("14:40","15:20","CHEM","Rm36"),
    ],
    4: [
        ("08:20","09:00","CHEM","Rm41"),
        ("09:00","09:40","CHEM","Rm41"),
        ("10:00","10:40","LIFE-ED","Rm41"),
        ("10:40","11:20","LIFE-ED","Rm41"),
        ("11:30","12:10","CHI","Rm41"),
        ("12:10","12:50","CHI","Rm41"),
        ("14:00","14:40","MATH","Rm41"),
        ("14:40","15:20","MATH","Rm41"),
    ],
    5: [
        ("08:20","09:00","PE","PlyGD"),
        ("09:00","09:40","PE","PlyGD"),
        ("10:00","10:40","CHEM","Rm41"),
        ("10:40","11:20","ENG","Rm41"),
        ("11:30","12:10","CHI","Rm41"),
        ("12:10","12:50","CSD","Rm41"),
        ("14:00","14:40","M2","Rm41"),
        ("14:40","15:20","M2","Rm41"),
    ],
    6: [
        ("08:20","09:00","M2","Rm41"),
        ("09:00","09:40","M2","Rm41"),
        ("10:00","10:40","CHI","Rm41"),
        ("10:40","11:20","CHI","Rm41"),
        ("11:30","12:10","CHEM","Rm41"),
        ("12:10","12:50","CSD","Rm41"),
        ("14:00","14:40","ENG","Rm41"),
        ("14:40","15:20","ENG","Rm41"),
    ],
    7: [
        ("08:20","09:00","M2","Rm41"),
        ("09:00","09:40","CSD","Rm41"),
        ("10:00","10:40","ENG","Rm41"),
        ("10:40","11:20","ENG","Rm41"),
        ("11:30","12:10","ICT","Rm51"),
        ("12:10","12:50","ICT","Rm51"),
        ("14:00","14:40","MATH","Rm41"),
        ("14:40","15:20","MATH","Rm41"),
    ],
}

HOLIDAYS = {
    "2025-10-01","2025-10-07","2025-10-29",
    "2025-11-24",
    "2025-12-08","2025-12-19",
    "2025-12-23","2025-12-24","2025-12-25","2025-12-26",
    "2025-12-29","2025-12-30","2025-12-31",
    "2026-01-01","2026-01-02","2026-01-05",
    "2026-02-16","2026-02-17","2026-02-18","2026-02-19",
    "2026-02-20","2026-02-23","2026-02-24",
    "2026-03-20",
    "2026-03-30","2026-03-31",
    "2026-04-01","2026-04-02","2026-04-03",
    "2026-04-06","2026-04-07","2026-04-08",
    "2026-05-01","2026-05-08","2026-05-25",
    "2026-06-19",
}

TEACHER_DAYS = {"2025-09-26","2026-03-20","2026-05-08"}
ALL_NO_SCHOOL = HOLIDAYS | TEACHER_DAYS


def get_cycle_day(target_date=None):
    if target_date is None:
        target_date = date.today()
    start = date.fromisoformat(CYCLE_START)
    if target_date < start:
        return None
    school_days = 0
    d = start
    while d <= target_date:
        if d.weekday() < 5 and d.isoformat() not in ALL_NO_SCHOOL:
            school_days += 1
        d += timedelta(days=1)
    return ((school_days - 2) % CYCLE_LENGTH) + 1 if school_days > 0 else None


def is_school_day(target_date=None):
    if target_date is None:
        target_date = date.today()
    return target_date.weekday() < 5 and target_date.isoformat() not in ALL_NO_SCHOOL


def get_next_school_day(from_date=None):
    d = (from_date or date.today()) + timedelta(days=1)
    while not is_school_day(d):
        d += timedelta(days=1)
    return d
