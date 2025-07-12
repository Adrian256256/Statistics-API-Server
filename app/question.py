"""
This module defines the Question dataclass.
"""
from dataclasses import dataclass

@dataclass
class Question:
    """
    This class represents a entry from a line in the csv file."
    """

    location: str
    year_start: int
    year_end: int
    question: str
    data_value: float
    stratification_category1: str
    stratification1: str
