from pydantic import BaseModel
from typing import List

class BookRecommendation(BaseModel):
    title: str
    summary: str

class TechTrend(BaseModel):
    trend: str
    explanation: str

class CombinedResponse(BaseModel):
    books: List[BookRecommendation]
    tech_trends: List[TechTrend]
    wiki_summary: str
