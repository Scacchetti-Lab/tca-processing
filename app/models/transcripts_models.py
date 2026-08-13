from pydantic import BaseModel as __BaseModel
from typing import List as __List
from constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, INSIGHT_PRIORITY, SCORE_TYPE, TRANSCRIPT_STATUS, TRANSCRIPT_TYPE

class TranscriptAnalyse(__BaseModel):
    status: TRANSCRIPT_STATUS
    type: TRANSCRIPT_TYPE
    score_type: SCORE_TYPE
    basic_description: __TranscriptDescription
    analytic: __AnalayseStrategicDefinitions | __AnalayseCustomerDefinitions
    feedback: str

class __Insights(__BaseModel):
    priority: INSIGHT_PRIORITY
    comment: str
    grade: int

class __TranscriptDescription(__BaseModel):
    company_name: str
    company_representor: str
    duration_min: int
    stakeholders: __List[str]
    meeting_summary: str
    insights: __Insights

class __AnalayseStrategicDefinitions(__BaseModel):
    employees_performance: float
    company_status: COMPANY_STATUS
    company_performance: float          
    closing_probability: float          
    problem_understanding: float        
    risk: float                         
    finacial_impact: float
    finacial_impact_status: FINANCIAL_STATUS

class __AnalayseCustomerDefinitions(__BaseModel):
    engagement: float                   
    opportunities_seized: float         
    communication_quality: float        
    objection_handling: float           
    converted_potencials: float         
    leads_converted: int
    tips: str