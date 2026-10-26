"""
Core search orchestrator interfacing with Exa AI Neural Search.
"""

import os
import sys
from typing import List, Dict, Any, Optional

from .constants import MUSIC_DOMAINS, DESIGN_DOMAINS, ALL_DOMAINS, ROLE_TEMPLATES
from .models import CreativeProspect, SearchConfig, EvaluationScore
from .evaluators import evaluate_candidate, generate_outreach_draft

class IndieScoutEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("EXA_API_KEY")
        self._exa = None

    def _get_client(self):
        if self._exa is None:
            if not self.api_key:
                raise ValueError(
                    "EXA_API_KEY is not set. Export EXA_API_KEY in your environment, "
                    "or pass api_key to IndieScoutEngine."
                )
            try:
                from exa_py import Exa
                self._exa = Exa(api_key=self.api_key)
            except ImportError:
                raise ImportError("exa_py is required. Run: pip install exa-py")
        return self._exa

    def build_prompt(self, role: str, vibe: str, region: str = "India") -> str:
        role_key = role.lower() if role.lower() in ROLE_TEMPLATES else "all"
        template = ROLE_TEMPLATES[role_key]
        return template.format(vibe=vibe, region=region)

    def resolve_domains(self, role: str) -> List[str]:
        r = role.lower()
        if r in ["music", "singer", "producer", "sound"]:
            return MUSIC_DOMAINS
        elif r in ["design", "designer", "illustrator", "ui", "brand", "3d"]:
            return DESIGN_DOMAINS
        return ALL_DOMAINS

    def scout(
        self,
        vibe: str,
        role: str = "music",
        region: str = "India",
        count: int = 5,
        app_name: str = "Our Startup",
        sender_name: str = "Founder"
    ) -> List[CreativeProspect]:
        client = self._get_client()
        query = self.build_prompt(role, vibe, region)
        domains = self.resolve_domains(role)

        response = client.search(
            query=query,
            type="neural",
            include_domains=domains,
            num_results=count,
            contents={"text": {"max_characters": 2500}}
        )

        prospects: List[CreativeProspect] = []
        for r in response.results:
            title = r.title or "Untitled Artist"
            text = r.text or ""
            url = r.url

            evaluation = evaluate_candidate(
                title=title,
                text=text,
                url=url,
                target_vibe=vibe,
                role=role
            )

            # Determine creator name
            name_parts = title.split("|")[0].split("-")[0].strip()
            creator_name = name_parts if len(name_parts) < 40 else "Creator"

            outreach = generate_outreach_draft(
                creator_name=creator_name,
                work_title=title[:40],
                app_name=app_name,
                role=role,
                vibe=vibe,
                sender_name=sender_name
            )

            prospect = CreativeProspect(
                creator_name=creator_name,
                creator_handle_or_id=None,
                role_archetype=role.capitalize(),
                city_region=region,
                primary_style_vibe=vibe,
                primary_portfolio_or_stream_url=url,
                signature_works=[title],
                why_they_fit_brief=text[:200].replace("\n", " ") + "...",
                evaluation=evaluation,
                outreach=outreach
            )
            prospects.append(prospect)

        return prospects
