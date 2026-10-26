"""
Tests for 5-Vector Evaluation Rubric and Outreach Generation.
"""

from indie_talent_scout.evaluators import evaluate_candidate, generate_outreach_draft
from indie_talent_scout.core import IndieScoutEngine

def test_evaluation_scoring():
    eval_result = evaluate_candidate(
        title="Honey Bee - Abhilasha Sinha",
        text="A dreamy acoustic summer bedroom pop release on Bandcamp. Contact for bookings: hello@artist.com",
        url="https://abhilashasinha.bandcamp.com/track/honey-bee",
        target_vibe="dreamy acoustic bedroom pop",
        role="singer"
    )

    assert eval_result.score_total >= 35
    assert eval_result.outreach_priority in ["High", "Medium"]
    assert eval_result.score_reachability >= 8

def test_outreach_generation():
    draft = generate_outreach_draft(
        creator_name="Abhilasha",
        work_title="Honey Bee",
        app_name="FinGlide",
        role="singer",
        vibe="dreamy acoustic indie",
        sender_name="Sriram"
    )

    assert "Abhilasha" in draft.instagram_dm
    assert "Honey Bee" in draft.email_body
    assert "FinGlide" in draft.email_subject

def test_prompt_builder():
    engine = IndieScoutEngine()
    prompt = engine.build_prompt("music", "lo-fi bedroom pop", "Delhi")
    assert "Delhi" in prompt
    assert "lo-fi bedroom pop" in prompt
    assert "Bandcamp" in prompt
