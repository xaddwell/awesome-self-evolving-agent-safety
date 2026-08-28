#!/usr/bin/env python3
"""Regenerate papers.json / stats.json for the SAVER project page.

Usage:
    python3 tools/gen_papers_json.py --csv data/saver_record_literature.csv --out .
"""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

VIOLATION_FAMILIES = [
    "Provenance Loss",
    "Authority Escalation",
    "Privacy & Purpose",
    "Persistent Descendants",
    "Operational Integrity",
    "Model Safety Regression",
]
RESPONSE_STAGES = [
    "Preventive Governance",
    "Transition & Activation",
    "Monitoring & Containment",
    "Recovery & Contestability",
]


def build_papers(rows: list[dict]) -> list[dict]:
    papers = []
    for r in rows:
        if not (r.get("title") and r.get("title", "").strip()):
            continue
        papers.append(
            {
                "id": r.get("paper_id", ""),
                "title": r["title"].strip(),
                "year": int(r["year"]) if r.get("year", "").isdigit() else None,
                "citation_key": r.get("citation_key", ""),
                "arxiv_id": r.get("arxiv_id", ""),
                "doi": r.get("doi", ""),
                "url": r.get("url", ""),
                "substrate": r.get("substrate", ""),
                "adaptation": r.get("adaptation", ""),
                "outcome": r.get("outcome", ""),
                "outcome_detail": r.get("outcome_detail", ""),
                "record_origin": r.get("record_origin", ""),
                "source_status": r.get("source_status", ""),
                "confidence": r.get("confidence", ""),
            }
        )
    papers.sort(key=lambda p: (p["year"] or 0, p["title"].lower()))
    return papers


def build_stats(rows: list[dict], papers: list[dict]) -> dict:
    usable = [r for r in rows if r.get("year", "").isdigit() and int(r["year"]) >= 2023]
    return {
        "coded_records": len(papers),
        "registry_works": sum(1 for r in rows if r.get("record_origin") == "registry"),
        "reviewed_cards": sum(1 for r in rows if r.get("record_origin") == "reviewed_card"),
        # audit snapshot of 14 June 2026; see the survey protocol appendix for the scoping method
        "screened_records": 583,
        "canonicalized_duplicates": 4,
        "usable_time_metadata": len(usable),
        "time_window": "2023 through 7 August 2026",
        "substrate_counts": dict(Counter(r.get("substrate") for r in rows if r.get("substrate"))),
        "adaptation_counts": dict(Counter(r.get("adaptation") for r in rows if r.get("adaptation"))),
        "outcome_counts": dict(Counter(r.get("outcome") for r in rows if r.get("outcome"))),
        "outcome_detail_counts": dict(
            Counter(r.get("outcome_detail") for r in rows if r.get("outcome_detail"))
        ),
        "violation_families": VIOLATION_FAMILIES,
        "response_stages": RESPONSE_STAGES,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/saver_record_literature.csv")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    papers = build_papers(rows)
    stats = build_stats(rows, papers)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "papers.json").write_text(json.dumps(papers, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(papers)} papers to {out / 'papers.json'}")
    print(f"wrote stats to {out / 'stats.json'}")


if __name__ == "__main__":
    main()
