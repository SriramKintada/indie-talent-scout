"""
5-Vector Evaluation and Outreach Generator for Indian Indie Creators.
"""

from typing import Dict, Any, List
from .models import EvaluationScore, OutreachDraft

def evaluate_candidate(
    title: str,
    text: str,
    url: str,
    target_vibe: str,
    role: str
) -> EvaluationScore:
    """
    Evaluates discovered candidate across 5 dimensions based on public evidence.
    """
    text_lower = (text or "").lower()
    title_lower = (title or "").lower()
    vibe_words = [w.lower() for w in target_vibe.split() if len(w) > 3]

    # Vector 1: Aesthetic fit (Keyword overlap and semantic alignment)
    fit_hits = sum(1 for w in vibe_words if w in text_lower or w in title_lower)
    score_aesthetic_fit = min(10, 6 + fit_hits * 2)

    # Vector 2: Authenticity (Flags for non-commercial, indie platforms)
    score_authenticity = 8
    if any(p in url for p in ["bandcamp.com", "neocities.org", "bento.me", "readcv.com"]):
        score_authenticity = 9
    if "agency" in text_lower or "commercial studio" in text_lower:
        score_authenticity = max(4, score_authenticity - 3)

    # Vector 3: Collaboration Realism
    score_collab_realism = 8
    if any(term in text_lower for term in ["open for commissions", "freelance", "contact for work", "bookings", "available"]):
        score_collab_realism = 10
    elif any(term in text_lower for term in ["represented by", "exclusive management", "record label booking"]):
        score_collab_realism = 5

    # Vector 4: Reachability
    score_reachability = 7
    if "@" in text_lower or "mailto:" in text_lower or "instagram" in text_lower:
        score_reachability = 9
    if "linktree" in text_lower or "bio.link" in text_lower:
        score_reachability = 10

    # Vector 5: Marketing Multiplier
    score_marketing_multiplier = 8
    if any(kw in text_lower for kw in ["award", "featured", "homegrown", "rolling stone", "unique", "distinctive"]):
        score_marketing_multiplier = 9

    total = (
        score_aesthetic_fit
        + score_authenticity
        + score_collab_realism
        + score_reachability
        + score_marketing_multiplier
    )

    if total >= 38:
        priority = "High"
    elif total >= 28:
        priority = "Medium"
    else:
        priority = "Low"

    return EvaluationScore(
        score_aesthetic_fit=score_aesthetic_fit,
        score_authenticity=score_authenticity,
        score_collab_realism=score_collab_realism,
        score_reachability=score_reachability,
        score_marketing_multiplier=score_marketing_multiplier,
        score_total=total,
        outreach_priority=priority,
    )

def generate_outreach_draft(
    creator_name: str,
    work_title: str,
    app_name: str,
    role: str,
    vibe: str,
    sender_name: str = "Founder"
) -> OutreachDraft:
    """Generates personalized Indian indie creator outreach drafts."""
    work_ref = f"'{work_title}'" if work_title else "your recent releases"

    dm = (
        f"Hey {creator_name}! Loved {work_ref}, especially the {vibe} feel. "
        f"So refreshing to see work with this level of craft coming out of India. "
        f"I am building {app_name}. We have budget set aside for our launch creative and "
        f"would love to explore a paid collaboration with you. "
        f"Let me know if you are open to a quick chat or where best to share details!"
    )

    email_sub = f"Paid collaboration: {app_name} x {creator_name}"
    email_body = (
        f"Hi {creator_name},\n\n"
        f"Came across your portfolio and was thoroughly impressed by {work_ref}. "
        f"The craft and intentionality stands out immediately.\n\n"
        f"I am {sender_name} at {app_name}. We are currently preparing our launch assets "
        f"and are looking for an independent {role} with your specific aesthetic to collaborate with.\n\n"
        f"Quick details:\n"
        f"- Scope: Bespoke creative project tailored around your signature style\n"
        f"- Commercials: Fully paid project at your standard professional rates\n"
        f"- Freedom: High creative autonomy, no corporate micromanagement\n\n"
        f"Would love to connect if you have bandwidth over the coming weeks.\n\n"
        f"Best,\n{sender_name}"
    )

    wa = (
        f"Hi {creator_name}, hope you are having a great week! I am {sender_name} from {app_name}. "
        f"Got your contact via your portfolio. Huge fan of {work_ref}! Sent you a short note "
        f"regarding a paid collaboration for our app launch. Whenever you get a moment, would love to connect."
    )

    return OutreachDraft(
        instagram_dm=dm,
        email_subject=email_sub,
        email_body=email_body,
        whatsapp_note=wa,
    )
