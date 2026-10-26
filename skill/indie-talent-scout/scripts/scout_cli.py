#!/usr/bin/env python3
"""
Indie Talent Scout CLI - Powered by Exa Neural Search
Scouts lowkey, high-craft Indian singers, music producers, and visual designers
for startups, founders, and creative teams.
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any

DOMAIN_PRESETS = {
    "music": [
        "bandcamp.com",
        "soundcloud.com",
        "open.spotify.com",
        "homegrown.co.in",
        "thewildcity.com",
        "rollingstoneindia.com",
        "youtube.com"
    ],
    "design": [
        "behance.net",
        "bento.me",
        "readcv.com",
        "layers.to",
        "neocities.org",
        "homegrown.co.in",
        "platform-mag.com"
    ],
    "all": [
        "bandcamp.com",
        "soundcloud.com",
        "behance.net",
        "bento.me",
        "readcv.com",
        "homegrown.co.in",
        "neocities.org"
    ]
}

def build_neural_query(role_type: str, vibe: str, region: str = "India") -> str:
    """Builds an Exa neural sentence completion prompt designed to match underground portfolios."""
    if role_type in ["music", "singer", "producer", "sound"]:
        return (
            f"Here is an independent indie singer, music producer, or songwriter from {region} "
            f"making {vibe} music on Bandcamp, SoundCloud, or Spotify:"
        )
    elif role_type in ["design", "designer", "illustrator", "ui", "brand", "3d"]:
        return (
            f"Here is the portfolio of an independent graphic designer, visual illustrator, or UI craftsman "
            f"based in {region} specializing in {vibe}:"
        )
    else:
        return f"Here is the personal portfolio of an independent creative artist based in {region} working on {vibe}:"

def run_scout_via_api(query: str, domains: List[str], num_results: int = 5) -> List[Dict[str, Any]]:
    """Runs search directly via exa_py if API key is configured."""
    try:
        from exa_py import Exa
    except ImportError:
        print("[!] exa_py not installed. Run: pip install exa-py", file=sys.stderr)
        return []

    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        print("[!] EXA_API_KEY environment variable is not set.", file=sys.stderr)
        print("[i] Use MCP tool `exa_search` directly in agent mode, or export EXA_API_KEY.", file=sys.stderr)
        return []

    exa = Exa(api_key=api_key)
    print(f"[*] Executing Exa neural search with query: '{query}'...", file=sys.stderr)
    
    response = exa.search(
        query=query,
        type="neural",
        include_domains=domains,
        num_results=num_results,
        contents={"text": {"max_characters": 2500}}
    )
    
    results = []
    for r in response.results:
        results.append({
            "title": r.title,
            "url": r.url,
            "author": getattr(r, "author", None),
            "published_date": getattr(r, "published_date", None),
            "snippet": r.text[:500] if r.text else "",
            "full_text": r.text
        })
    return results

def format_markdown_report(results: List[Dict[str, Any]], role_type: str, vibe: str) -> str:
    lines = [
        f"# Indie Talent Scouting Dossier",
        f"**Target Role:** {role_type.upper()} | **Aesthetic / Vibe:** {vibe}",
        f"**Candidates Discovered:** {len(results)}\n",
        "| Candidate / Title | Platform Link | Style & Craft Signal |",
        "| :--- | :--- | :--- |"
    ]
    for r in results:
        title = r.get("title", "Untitled").replace("|", "-")
        url = r.get("url", "#")
        snippet = r.get("snippet", "").replace("\n", " ")[:150] + "..."
        lines.append(f"| **{title}** | [{url}]({url}) | {snippet} |")
    
    lines.append("\n## Next Actions:")
    lines.append("1. Verify public contact route (IG DM / Linktree / Email).")
    lines.append("2. Score candidates against the 5-Vector Rubric in `references/scoring_rubric.md`.")
    lines.append("3. Deploy personalized pitch from `templates/outreach_playbook.md`.")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Scout lowkey indie talent in India with Exa")
    parser.add_argument("--role", choices=["music", "singer", "producer", "design", "designer", "illustrator", "ui", "all"], default="music", help="Role archetype to search")
    parser.add_argument("--vibe", type=str, required=True, help="Specific aesthetic, sound, or design style description")
    parser.add_argument("--region", type=str, default="India", help="Geographic focus (e.g. India, Bangalore, Delhi, Kerala)")
    parser.add_argument("--count", type=int, default=5, help="Number of prospects to return (1-20)")
    parser.add_argument("--format", choices=["markdown", "json", "prompt-only"], default="markdown", help="Output format")
    
    args = parser.parse_args()
    
    category_key = "music" if args.role in ["music", "singer", "producer"] else "design" if args.role != "all" else "all"
    domains = DOMAIN_PRESETS.get(category_key, DOMAIN_PRESETS["all"])
    query = build_neural_query(args.role, args.vibe, args.region)
    
    if args.format == "prompt-only":
        print(json.dumps({
            "query": query,
            "type": "neural",
            "include_domains": domains,
            "num_results": args.count
        }, indent=2))
        return

    results = run_scout_via_api(query, domains, args.count)
    if not results:
        print("[!] No results returned via CLI directly. In Antigravity/OpenClaw, invoke Exa MCP with these parameters:")
        print(f"    Tool: call_mcp_tool(ServerName='exa', ToolName='exa_search')")
        print(f"    Query: '{query}'")
        print(f"    Include Domains: {domains}")
        return

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(format_markdown_report(results, args.role, args.vibe))

if __name__ == "__main__":
    main()
