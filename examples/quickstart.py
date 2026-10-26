"""
Quickstart example for indie-talent-scout.
"""

import os
from indie_talent_scout import IndieScoutEngine

def main():
    # Make sure EXA_API_KEY is exported, or pass it directly to IndieScoutEngine(api_key="...")
    engine = IndieScoutEngine()

    print("[*] Generating neural query parameters for prompt preview...")
    query = engine.build_prompt(role="singer", vibe="wistful acoustic bedroom pop", region="Bangalore")
    print(f"Generated Exa Prompt: {query}\n")

    if not os.environ.get("EXA_API_KEY"):
        print("[!] Note: Export EXA_API_KEY to execute live searches.")
        return

    print("[*] Scouting live candidates...")
    prospects = engine.scout(
        vibe="wistful acoustic bedroom pop",
        role="singer",
        region="Bangalore",
        count=3,
        app_name="Aura Audio"
    )

    for p in prospects:
        print(f"Candidate: {p.creator_name} ({p.role_archetype})")
        print(f"Score: {p.evaluation.score_total}/50 | Priority: {p.evaluation.outreach_priority}")
        print(f"URL: {p.primary_portfolio_or_stream_url}")
        if p.outreach:
            print(f"DM Hook: {p.outreach.instagram_dm}\n")

if __name__ == "__main__":
    main()
