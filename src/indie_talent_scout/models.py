"""
Pydantic data models for Indian creative talent scouting.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class EvaluationScore(BaseModel):
    score_aesthetic_fit: int = Field(ge=0, le=10, description="Depth and polish alignment with brief")
    score_authenticity: int = Field(ge=0, le=10, description="Underground craft, low follower vanity")
    score_collab_realism: int = Field(ge=0, le=10, description="Independent status, openness to projects")
    score_reachability: int = Field(ge=0, le=10, description="Direct email, Linktree, or open DM access")
    score_marketing_multiplier: int = Field(ge=0, le=10, description="Brand elevation when paired with app")
    score_total: int = Field(ge=0, le=50, description="Sum of 5 vectors")
    outreach_priority: Literal["High", "Medium", "Low"] = Field(description="Priority classification")

class OutreachDraft(BaseModel):
    instagram_dm: str
    email_subject: str
    email_body: str
    whatsapp_note: str

class CreativeProspect(BaseModel):
    creator_name: str
    creator_handle_or_id: Optional[str] = None
    role_archetype: str
    city_region: str = "India"
    primary_style_vibe: str
    primary_portfolio_or_stream_url: str
    follower_or_scale_estimate: str = "Underground (<25k)"
    signature_works: List[str] = Field(default_factory=list)
    contact_channel: Literal["Instagram DM", "Direct Email", "Linktree / WhatsApp", "Behance Message", "Other"] = "Instagram DM"
    contact_address_or_link: Optional[str] = None
    independence_status: Literal["Independent / Self-managed", "Likely Independent", "Partially Managed", "Agency / Label Locked"] = "Independent / Self-managed"
    why_they_fit_brief: str
    evaluation: EvaluationScore
    outreach: Optional[OutreachDraft] = None

class SearchConfig(BaseModel):
    role: str = "music"
    vibe: str
    region: str = "India"
    count: int = Field(default=5, ge=1, le=25)
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None
