from pydantic import BaseModel
from typing import List
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, INSIGHT_PRIORITY, SCORE_TYPE, TRANSCRIPT_STATUS, TRANSCRIPT_TYPE

class Insights(BaseModel):    
    priority: INSIGHT_PRIORITY
    comment: str
    grade: int

class TranscriptDescription(BaseModel):
    company_name: str
    company_representor: str
    duration_min: int
    stakeholders: List[str]
    meeting_summary: str
    insights: Insights

class AnalayseStrategicDefinitions(BaseModel):
    company_performance: float          
    closing_probability: float          
    flexibility: float
    risk: float                         
    finacial_impact: float
    finacial_impact_value: float
    finacial_impact_status: FINANCIAL_STATUS
    company_status: COMPANY_STATUS    

class AnalayseCustomerDefinitions(BaseModel):
    engagement: float                   
    communication_quality: float        
    opportunities_seized: float         
    objection_handling: float           
    errors_missed_opportunities: float         
    leads_converted: int
    tips: str

class TranscriptAnalyse(BaseModel):
    status: TRANSCRIPT_STATUS
    type: TRANSCRIPT_TYPE
    score_type: SCORE_TYPE
    basic_description: TranscriptDescription
    analytic: AnalayseStrategicDefinitions | AnalayseCustomerDefinitions
    feedback: str

class TranscriptReturnJson(BaseModel):
    transcription: str
    meeting_date: str
    revenue: str
    unit_name: str
    score_type: SCORE_TYPE

class TranscriptPayload(BaseModel):
    transcript: str
    score_type: SCORE_TYPE | None = None