from pydantic import BaseModel
from app.constants.transcript import FINANCIAL_STATUS

class MeetingPerformanceDto(BaseModel):
    engagement: float
    communication_quality: float
    opportunities_seized: float
    objection_handling: float
    missed_opportunities: float
    feedback: str
    tips: str

class MeetingStrategicDto(BaseModel):
    closing_probability: float
    flexibility: float
    risk: float
    financial_impact: float # value
    financial_impact_status: FINANCIAL_STATUS
    tips: str
    feedback: str