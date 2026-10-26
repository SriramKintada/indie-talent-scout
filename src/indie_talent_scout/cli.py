"""
Rich CLI interface for indie-talent-scout.
"""

import sys
import json
import argparse
from typing import List

from .core import IndieScoutEngine
from .constants import ROLE_TEMPLATES, MUSIC_DOMAINS, DESIGN_DOMAINS, ALL_DOMAINS
from .models import CreativeProspect

def render_rich_table(prospects: List[CreativeProspect]):
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel

        console = Console()
        table = Table(title="[bold cyan]Indie Talent Scout: Discovered Prospects[/bold cyan]", show_header=True)
        table.add_column("Score", style="bold green", justify="center")
        table.add_column("Priority", style="bold yellow", justify="center")
        table.add_column("Creator / Act", style="bold white")
        table.add_column("Role", style="magenta")
        table.add_column("Platform / Portfolio URL", style="blue")

        for p in prospects:
            table.add_row(
                f"{p.evaluation.score_total}/50",
                p.evaluation.outreach_priority,
                p.creator_name,
                p.role_archetype,
                p.primary_portfolio_or_stream_url
            )

        console.print("\n")
        console.print(table)
        console.print("\n[bold green]Sample Outreach Draft (Top Candidate):[/bold green]")
        if prospects and prospects[0].outreach:
            console.print(Panel(prospects[0].outreach.instagram_dm, title="[yellow]Instagram DM Hook[/yellow]"))
        console.print("\n")
    except ImportError:
        # Fallback to plain text
        print("\n=== Discovered Prospects ===")
        for p in prospects:
            print(f"[{p.evaluation.score_total}/50 | {p.evaluation.outreach_priority}] {p.creator_name} ({p.role_archetype})")
            print(f"  URL: {p.primary_portfolio_or_stream_url}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Scout lowkey, high-craft Indian singers, music producers, and visual designers using Exa AI."
    )
    parser.add_argument(
        "--role",
        choices=["music", "singer", "producer", "sound", "design", "designer", "illustrator", "ui", "brand", "all"],
        default="music",
        help="Creative role archetype to scout"
    )
    parser.add_argument("--vibe", type=str, required=True, help="Specific aesthetic, sound, or visual style description")
    parser.add_argument("--region", type=str, default="India", help="Geographic scene (e.g. India, Bangalore, Delhi, Kerala)")
    parser.add_argument("--count", type=int, default=5, help="Number of prospects to return (1-20)")
    parser.add_argument("--app-name", type=str, default="Our Startup", help="Name of your app/startup for outreach generation")
    parser.add_argument("--format", choices=["table", "json", "markdown", "prompt-only"], default="table", help="Output format")

    args = parser.parse_args()

    engine = IndieScoutEngine()

    if args.format == "prompt-only":
        prompt = engine.build_prompt(args.role, args.vibe, args.region)
        domains = engine.resolve_domains(args.role)
        print(json.dumps({
            "query": prompt,
            "type": "neural",
            "include_domains": domains,
            "num_results": args.count
        }, indent=2))
        return

    try:
        prospects = engine.scout(
            vibe=args.vibe,
            role=args.role,
            region=args.region,
            count=args.count,
            app_name=args.app_name
        )
    except ValueError as e:
        print(f"\n[!] Configuration Error: {e}", file=sys.stderr)
        print("To preview the generated search parameters without an API key, use --format prompt-only", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] Search Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        print(json.dumps([p.model_dump() for p in prospects], indent=2))
    elif args.format == "markdown":
        print(f"# Talent Scout Shortlist: {args.role.upper()} ({args.vibe})\n")
        print("| Score | Priority | Creator | Portfolio / URL |")
        print("| :---: | :---: | :--- | :--- |")
        for p in prospects:
            print(f"| {p.evaluation.score_total}/50 | {p.evaluation.outreach_priority} | {p.creator_name} | {p.primary_portfolio_or_stream_url} |")
    else:
        render_rich_table(prospects)

if __name__ == "__main__":
    main()
