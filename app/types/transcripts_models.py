from __future__ import annotations
from pydantic import BaseModel
from typing import List
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, INSIGHT_PRIORITY, PROFILE_TYPES, SCORE_TYPE, TRANSCRIPT_STATUS

class Insights(BaseModel):    
    priority: INSIGHT_PRIORITY
    avg_grande: int
    tips: str

class TranscriptDescription(BaseModel):
    company_name: str
    company_representor: str
    stakeholders: List[str]
    meeting_summary: str

class AnalayseStrategicDefinitions(BaseModel):                      
    metrics: AnalyseStrategicMetrics
    financial: AnalyseStrategicFinancial
    company_status: COMPANY_STATUS
    insights: Insights    
    feedback: str

class AnalyseStrategicFinancial(BaseModel):
    financial_impact: float
    financial_impact_value: float
    financial_impact_status: FINANCIAL_STATUS

class AnalyseStrategicMetrics(BaseModel):
    company_performance: float          
    closing_probability: float          
    flexibility: float
    risk: float

class AnalayseCustomerDefinitions(BaseModel):
    metrics: AnalayseCustomerMetrics
    insights: Insights
    segment: str
    feedback: str

class AnalayseCustomerMetrics(BaseModel):
    engagement: float
    communication_quality: float
    opportunities_seized: float
    objection_handling: float
    missed_opportunities: float
    leads_converted: int

class TranscriptAnalyse(BaseModel):
    status: TRANSCRIPT_STATUS
    basic_description: TranscriptDescription
    analytic: Analytics

class Analytics(BaseModel):
    strategic: AnalayseStrategicDefinitions
    performance: AnalayseCustomerDefinitions

class TranscriptReturnJson(BaseModel):
    transcription: str
    meeting_date: str
    revenue: str
    totvs_unit: str
    score_type: SCORE_TYPE

class TranscriptPayload(BaseModel):
    transcript: str
    profile: PROFILE_TYPES | None = None