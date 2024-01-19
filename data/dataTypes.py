from typing import TypedDict

class gradeData(TypedDict):
    aprec: float
    bprec: float
    cprec: float
    dprec: float
    fprec: float

MathGrades: gradeData = {"aprec": 0.0, "bprec": 0.0, "cprec": 0.0, "dprec": 0.0, "fprec": 0.0}
FalseGrades: gradeData = {"number": 5.5}
print(FalseGrades)
