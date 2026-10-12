from __future__ import annotations
from pydantic import BaseModel
from typing import List, Literal
from app.constants.transcript import COMPANY_STATUS, FINANCIAL_STATUS, INSIGHT_PRIORITY, PROFILE_TYPES, SCORE_TYPE, TRANSCRIPT_DB_STATUS
from app.types.client_models import ClientContext

class Stakeholder(BaseModel):
    name: str
    role: str | None = None
    side: Literal['CLIENT', 'COMPANY', 'UNKNOWN']

class Insights(BaseModel):    
    priority: INSIGHT_PRIORITY
    rating: int
    tips: str

class TranscriptDescription(BaseModel):
    company_name: str
    company_representor: str
    segment: str
    stakeholders: List[Stakeholder]
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
    feedback: str

class AnalayseCustomerMetrics(BaseModel):
    engagement: float
    communication_quality: float
    opportunities_seized: float
    objection_handling: float
    missed_opportunities: float
    leads_converted: int

class TranscriptAnalyse(BaseModel):
    status: TRANSCRIPT_DB_STATUS
    basic_description: TranscriptDescription
    analytic: Analytics

class Analytics(BaseModel):
    strategic: AnalayseStrategicDefinitions | None = None
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
    client: ClientContext | None = None
    scope: Literal["EXTERNAL", "INTERNAL"]

class TranscriptRequest(BaseModel):
    transcript_id: str
    profile: PROFILE_TYPES | None = None
    client_context: ClientContext | None = None
    scope: Literal["EXTERNAL", "INTERNAL"]