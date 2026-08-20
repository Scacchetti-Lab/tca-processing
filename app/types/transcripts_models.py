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
    employees_performance: float
    company_status: COMPANY_STATUS
    company_performance: float          
    closing_probability: float          
    problem_understanding: float        
    risk: float                         
    finacial_impact: float
    finacial_impact_status: FINANCIAL_STATUS

class AnalayseCustomerDefinitions(BaseModel):
    engagement: float                   
    opportunities_seized: float         
    communication_quality: float        
    objection_handling: float           
    converted_potencials: float         
    leads_converted: int
    tips: str

class TranscriptAnalyse(BaseModel):
    status: TRANSCRIPT_STATUS
    type: TRANSCRIPT_TYPE
    score_type: SCORE_TYPE
    basic_description: TranscriptDescription
    analytic: AnalayseStrategicDefinitions | AnalayseCustomerDefinitions
    feedback: str