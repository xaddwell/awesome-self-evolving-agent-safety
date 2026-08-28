#!/usr/bin/env python3
"""Generate the SAVER survey project-page data from the manuscript sources.

Inputs (canonical, inside the manuscript workspace):
  * draft/figures/data/saver_record_literature.csv      -- coded pool
  * draft/table_vocabulary.tex                          -- table label macros
  * draft/tables/*.tex                                  -- classification tables
  * draft/figures/saver_transition_roadmap.tex          -- roadmap tree

Outputs (under OUT_DIR, copied verbatim to the project page):
  * papers.json          -- one record per coded paper
  * stats.json           -- corpus aggregates
  * tables.json          -- classification tables converted to web markup
  * roadmap.json         -- roadmap tree parsed from the TikZ source
"""

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_CSV = REPO / "data" / "saver_record_literature.csv"
DEFAULT_VOCAB = REPO / "source" / "table_vocabulary.tex"
DEFAULT_TABLES = [
    "substrate_literature_index",
    "adaptation_literature_index",
    "violation_literature_index",
    "violation_exposure_literature_index",
    "response_literature_index",
    "evaluation_literature_index",
    "lifecycle_coverage_matrix",
    "benchmark_saver_coverage_matrix",
]
DEFAULT_ROADMAP = REPO / "source" / "roadmap.tex"
OUT_DIR = REPO / ".tmp" / "saver_page"  # unused for the vendored copy; --out defaults to the repo root

LANE_COLORS = {
    "saver-blue-bg": "#527CDF",
    "saver-green-bg": "#86D4CD",
    "saver-orange-bg": "#E9A859",
    "saver-red-bg": "#E2707C",
}
HEAD_COLORS = {
    "saverNeutralHead": "#E9EEF5",
    "saverSubstrateHead": "#E6EEFF",
    "saverAdaptationHead": "#E7F5EF",
    "saverViolationHead": "#FCEAEC",
    "saverExposureHead": "#F0E8FA",
    "saverResponseHead": "#E4F3F1",
    "saverEvaluationHead": "#FFF3DC",
}
ROLE_COLORS = {
    "tableRoleAttack": "#C75B66",
    "tableRoleDefense": "#3F9B8F",
    "tableRoleGovernance": "#5B8FA8",
    "tableRoleBenchmark": "#C2914B",
    "tableRoleSafety": "#9B7FBD",
    "tableRoleCapability": "#7A8B94",
    "tableRoleSurvey": "#8A97A8",
    "tableRoleFramework": "#6D93AC",
    "tableRoleTheory": "#B09A5F",
    "tableRoleRedTeam": "#C47163",
}
CHIP_COLORS = {
    "tableChipBack": "#E9EFF2",
    "tableChipMemory": "#9CC0FF",
    "tableChipTool": "#7FD6C0",
    "tableChipWorkflow": "#EDC884",
    "tableChipModel": "#C9A8E8",
    "tableChipRuntime": "#9DC3D8",
}
SYMBOLS = {"covYes": ("✓", "direct"), "covPart": ("◐", "partial"), "covNo": ("○", "mostly absent"),
           "HYes": ("✓", "direct"), "HPart": ("◐", "partial"), "HNo": ("○", "mostly absent")}


# --------------------------------------------------------------------------- #
#  tiny LaTeX parser for cell text (commands with balanced-brace args)         #
# --------------------------------------------------------------------------- #

class CellParser:
    def __init__(self, vocab: dict[str, str]):
        self.vocab = vocab
        self.refs: list[str] = []

    def parse(self, text: str) -> str:
        out: list[str] = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            if ch == "\\":
                m = re.match(r"\\[a-zA-Z]+\*?", text[i:])
                if not m:
                    out.append("\\")
                    i += 1
                    continue
                cmd = m.group(0)[1:].rstrip("*")
                i += len(m.group(0))
                args: list[str] = []
                while i < n and text[i].isspace() and cmd not in (" ",):
                    i += 1
                j = i
                while j < n and text[j] == "{":
                    end = self._match_brace(text, j)
                    args.append(text[j + 1 : end])
                    j = end + 1
                    while j < n and text[j].isspace():
                        j += 1
                i = j
                out.append(self._dispatch(cmd, args))
            elif ch == "$":
                end = text.find("$", i + 1)
                if end == -1:
                    out.append(ch)
                    i += 1
                else:
                    out.append(self._math(text[i + 1 : end]))
                    i = end + 1
            elif ch == "~":
                out.append(" ")
                i += 1
            else:
                out.append(ch)
                i += 1
        return "".join(out)

    @staticmethod
    def _match_brace(text: str, start: int) -> int:
        depth = 0
        for k in range(start, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    return k
        return len(text) - 1

    def _dispatch(self, cmd: str, args: list[str]) -> str:
        if cmd in ("cite", "citep"):
            keys = [k.strip() for k in (args[0] if args else "").split(",") if k.strip()]
            self.refs.extend(keys)
            return ""
        if cmd in ("apptabref", "tabref", "figref", "appfigref", "secref", "Secref", "ref", "label"):
            return ""
        if cmd in ("textbf", "emph", "textsf"):
            return f"<b>{self.parse(args[0])}</b>" if cmd == "textbf" else (
                f"<i>{self.parse(args[0])}</i>" if cmd == "emph" else self.parse(args[0]))
        if cmd == "textcolor" and len(args) >= 2:
            rc = ROLE_COLORS.get(args[0], args[0])
            return f'<span class="role" style="--rc:{rc}">{self.parse(args[1])}</span>'
        if cmd == "TableRoleTag" and len(args) >= 2:
            rc = ROLE_COLORS.get(args[0], args[0])
            return f'<span class="role" style="--rc:{rc}">{self.parse(args[1])}</span>'
        if cmd == "TableTargetTag" and args:
            return f'<span class="target">{self.parse(args[0])}</span>'
        if cmd == "TablePill" and len(args) >= 3:
            cc = CHIP_COLORS.get(args[0], args[0])
            return f'<span class="chip" style="--cc:{cc}">{self.parse(args[2])}</span>'
        if cmd == "TableChip" and len(args) >= 2:
            cc = CHIP_COLORS.get(args[0], args[0])
            return f'<span class="chip" style="--cc:{cc}">{self.parse(args[1])}</span>'
        chip_specific = {
            "TablePlainChip": "tableChipBack",
            "TableMemoryChip": "tableChipMemory",
            "TableToolChip": "tableChipTool",
            "TableWorkflowChip": "tableChipWorkflow",
            "TableModelChip": "tableChipModel",
            "TableRuntimeChip": "tableChipRuntime",
        }
        if cmd in chip_specific and args:
            cc = CHIP_COLORS[chip_specific[cmd]]
            return f'<span class="chip" style="--cc:{cc}">{self.parse(args[0])}</span>'
        if cmd == "TableAdaptationOp" and args:
            return f'<span class="chip" style="--cc:#A8D5BE">{self.parse(args[0])}</span>'
        if cmd in SYMBOLS:
            sym, tip = SYMBOLS[cmd]
            return f'<span class="cov" title="{tip}">{sym}</span>'
        if cmd == "SAVER":
            return "SAVER"
        if cmd in self.vocab:
            return self.parse(self.vocab[cmd])
        if cmd in ("HYes", "HPart", "HNo"):
            return self._dispatch(cmd, args)
        # unknown command: drop the command, keep argument text
        return self.parse(" ".join(args))

    def _math(self, expr: str) -> str:
        expr = expr.replace("\\rightarrow", "→").replace("\\to", "→")
        expr = expr.replace("\\times", "×").replace("\\leftarrow", "←")
        expr = expr.replace("\\ell", "ℓ").replace("\\delta", "δ")
        expr = expr.replace("\\mathcal", "").replace("\\mathbf", "").replace("\\mathrm", "")
        expr = re.sub(r"\\sb\{([^}]*)\}", r"<sub>\1</sub>", expr)
        expr = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", expr)
        expr = re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", expr)
        expr = re.sub(r"\\[a-zA-Z]+", "", expr)
        expr = expr.replace("{", "").replace("}", "")
        return expr


# --------------------------------------------------------------------------- #
#  vocabulary                                                                    #
# --------------------------------------------------------------------------- #

def load_vocab(path: Path, extra_sources: list[Path] | None = None) -> dict[str, str]:
    vocab: dict[str, str] = {}
    sources = [path] + (extra_sources or [])

    def macro_body(text: str, start: int) -> str:
        """Return the balanced-brace body starting at text[start] (a '{')."""
        depth = 0
        for k in range(start, len(text)):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
                if depth == 0:
                    return text[start + 1 : k]
        return ""

    for src in sources:
        text = src.read_text(encoding="utf-8")
        for m in re.finditer(r"\\newcommand\{\\([a-zA-Z]+)\}\{", text):
            body = macro_body(text, m.end() - 1)
            if body:
                vocab[m.group(1)] = body
    # expand one level for primitive wrappers
    for key, body in list(vocab.items()):
        for other, val in vocab.items():
            if f"\\{other}" in body and other not in ("TableRoleTag", "TableTargetTag", "TablePill"):
                body = body.replace(f"\\{other}", val)
        vocab[key] = body
    return vocab


# --------------------------------------------------------------------------- #
#  classification tables                                                          #
# --------------------------------------------------------------------------- #

def ref_links(refs: list[str], papers_by_key: dict[str, dict]) -> str:
    if not refs:
        return ""
    parts = []
    for k in refs:
        p = papers_by_key.get(k)
        if p and p.get("arxiv_id"):
            parts.append(
                f'<sup><a class="tref" href="https://arxiv.org/abs/{p["arxiv_id"]}" target="_blank" rel="noopener" '
                f'title="{p["title"]} ({p.get("year") or "n.d."})">[{p["arxiv_id"]}]</a></sup>'
            )
        elif p and p.get("url"):
            parts.append(
                f'<sup><a class="tref" href="{p["url"]}" target="_blank" rel="noopener" '
                f'title="{p["title"]} ({p.get("year") or "n.d."})">[ref]</a></sup>'
            )
        else:
            parts.append(f'<sup><span class="tref" title="{k}">[{k}]</span></sup>')
    return "".join(parts)


def convert_table(tex: str, parser: CellParser, papers_by_key: dict[str, dict]) -> dict | None:
    cap = re.search(r"\\caption\{((?:[^{}]|\{[^{}]*\})*)\}", tex, flags=re.S)
    caption = parser.parse(cap.group(1)) if cap else ""
    m = re.search(r"\\begin\{tabular\}", tex)
    if not m:
        return None
    # skip the balanced column-spec brace group (the '{' sits at m.end())
    colspec_end = parser._match_brace(tex, m.end())
    tab = re.search(r"\\end\{tabular\}", tex)
    if not tab:
        return None
    body = tex[colspec_end + 1 : tab.start()]
    body = re.sub(r"\\resizebox\{[^}]*\}\{[^}]*\}\{\%?", "", body)
    body = re.sub(r"\\toprule|\\bottomrule|\\midrule|\\cmidrule[^\n]*", "", body)
    body = re.sub(r"\\addlinespace\[[^\]]*\]", "", body)
    body = re.sub(r"\\SAVERTableRows|\\SAVERTableReset|\\rowcolors[^\n]*", "", body)
    body = body.rstrip().rstrip("}").rstrip("%").rstrip()

    rows_out: list[dict] = []
    groups: list[tuple[str, int, str]] = []
    def _group_repl(m: re.Match) -> str:
        groups.append((m.group(1), int(m.group(2)), m.group(3)))
        return ""
    body = re.sub(r"\\SAVERTableGroup\{([^}]*)\}\{(\d+)\}\{([^}]*)\}", _group_repl, body)
    raw_rows = re.split(r"\\\\", body)
    group_idx = 0
    for raw in raw_rows:
        raw = raw.strip()
        if not raw:
            if group_idx < len(groups):
                color, span, text = groups[group_idx]
                rows_out.append({"type": "group", "color": HEAD_COLORS.get(color, color),
                                 "span": span, "text": parser.parse(text)})
                group_idx += 1
            continue
        if group_idx < len(groups):
            color, span, text = groups[group_idx]
            rows_out.append({"type": "group", "color": HEAD_COLORS.get(color, color),
                             "span": span, "text": parser.parse(text)})
            group_idx += 1
        cells_raw = raw.split("&")
        cells: list[dict] = []
        for cell in cells_raw:
            cell = cell.strip()
            cell = re.sub(r"\\rowcolor\{[^}]*\}", "", cell)
            head_cls = ""
            mcell = re.match(r"\\cellcolor\{([^}]*)\}", cell)
            if mcell:
                head_cls = HEAD_COLORS.get(mcell.group(1), "")
                cell = cell[mcell.end():].strip()
            colspan = 1
            mcol = re.match(r"\\multicolumn\{(\d+)\}\{[^}]*\}\{(.*)\}\s*$", cell, flags=re.S)
            if mcol:
                colspan = int(mcol.group(1))
                cell = mcol.group(2)
            bold = cell.startswith("\\textbf") or re.match(r"^\\textbf", cell) is not None
            parser.refs = []
            html = parser.parse(cell.strip()).strip()
            html = html.replace("~", " ").replace("\\&", "&amp;").replace("\\%", "%").replace("\\_", "_")
            cells.append({"html": html, "colspan": colspan, "head": head_cls, "refs": list(parser.refs)})
        rows_out.append({"type": "row", "cells": cells})

    header = None
    body_rows = []
    for r in rows_out:
        if r["type"] == "row" and header is None and any("textbf" in c["html"] or "<b>" in c["html"] for c in r["cells"]):
            header = r
        else:
            body_rows.append(r)
    return {"header": header, "rows": body_rows, "caption": caption}


# --------------------------------------------------------------------------- #
#  roadmap tree                                                                  #
# --------------------------------------------------------------------------- #

def parse_roadmap(tex: str) -> dict:
    forest = re.search(r"\\begin\{forest\}(.*?)\\end\{forest\}", tex, flags=re.S)
    if not forest:
        return {"name": "SAVER Roadmap", "children": []}
    content = forest.group(1)

    def nodes_from(text: str):
        stack: list[dict] = []
        root: dict | None = None
        buf: list[str] = []
        brace = 0
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == "{" :
                brace += 1
                buf.append(ch)
            elif ch == "}":
                brace -= 1
                buf.append(ch)
            elif ch == "[" and brace == 0:
                if stack and not stack[-1].get("_sealed"):
                    stack[-1]["name"] = "".join(buf).strip()
                    stack[-1]["_sealed"] = True
                buf = []
                stack.append({"name": "", "children": [], "_depth": len(stack)})
                i += 1
                continue
            elif ch == "]" and brace == 0 and stack:
                node = stack.pop()
                if not node.get("_sealed"):
                    node["name"] = "".join(buf).strip()
                buf = []
                if stack:
                    stack[-1]["children"].append(node)
                else:
                    root = node
                i += 1
                continue
            else:
                if stack:
                    buf.append(ch)
            i += 1
        return root

    root = nodes_from(content)
    if root is None:
        return {"name": "SAVER Roadmap", "children": []}

    def clean(raw: str):
        styles = []
        text = raw
        while True:
            m = re.search(r",\s*((?:par|saver-[a-z-]+))\s*$", text)
            if not m:
                break
            styles.append(m.group(1))
            text = text[: m.start()].rstrip()
        refs: list[str] = []
        for m in re.finditer(r"\\saverRoadmapCite\{([^}]*)\}", text):
            refs.extend(k.strip() for k in m.group(1).split(",") if k.strip())
        text = re.sub(r"\\saverRoadmapCite\{[^}]*\}", "", text)
        text = re.sub(r"\\saverRoadmapRefRange\{[^}]*\}\{[^}]*\}", "", text)
        text = re.sub(r"\\saverRoadmapRef\{[^}]*\}", "", text)
        text = text.replace("\\SAVER", "SAVER")
        text = text.replace("$\\rightarrow$", "→").replace("~", " ")
        text = re.sub(r"\\[a-zA-Z]+", "", text)
        text = text.strip("{}").strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text).strip(", ")
        return text, styles, refs

    def build(node: dict, depth: int) -> dict:
        name, styles, refs = clean(node.get("name", ""))
        kind = "root"
        color = "#9BA4B5"
        if "saver-root" in styles:
            kind, color = "root", "#9BA4B5"
        elif any(s in LANE_COLORS for s in styles):
            kind = "lane"
            color = next(LANE_COLORS[s] for s in styles if s in LANE_COLORS)
        elif any(s.endswith("-line") for s in styles):
            kind = "path"
        elif "saver-violation-leaf" in styles:
            kind, color = "violation", "#E2707C"
        elif "saver-response-leaf" in styles:
            kind, color = "response", "#2F7F73"
        return {
            "name": name or ("SAVER Roadmap" if kind == "root" else ""),
            "kind": kind,
            "color": color,
            "refs": refs,
            "children": [build(c, depth + 1) for c in node.get("children", [])],
        }

    return build(root, 0)


# --------------------------------------------------------------------------- #
#  main                                                                         #
# --------------------------------------------------------------------------- #

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(DEFAULT_CSV))
    ap.add_argument("--vocab", default=str(DEFAULT_VOCAB))
    ap.add_argument("--tables-dir", default=str(REPO / "source" / "tables"))
    ap.add_argument("--tables", default=",".join(DEFAULT_TABLES))
    ap.add_argument("--roadmap", default=str(DEFAULT_ROADMAP))
    ap.add_argument("--out", default=str(REPO))
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    papers = []
    for r in rows:
        if not (r.get("title") and r.get("title", "").strip()):
            continue
        papers.append({
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
        })
    papers.sort(key=lambda p: (p["year"] or 0, p["title"].lower()))
    papers_by_key = {p["citation_key"]: p for p in papers if p["citation_key"]}

    usable = [r for r in rows if r.get("year", "").isdigit() and int(r["year"]) >= 2023]
    stats = {
        "coded_records": len(papers),
        "registry_works": sum(1 for r in rows if r.get("record_origin") == "registry"),
        "reviewed_cards": sum(1 for r in rows if r.get("record_origin") == "reviewed_card"),
        "screened_records": 583,
        "canonicalized_duplicates": 4,
        "usable_time_metadata": len(usable),
        "time_window": "2023 through 7 August 2026",
    }

    vocab_path = Path(args.vocab)
    table_dir = Path(args.tables_dir)
    extra_vocab_sources = [table_dir / f"{name}.tex" for name in args.tables.split(",")]
    vocab = load_vocab(vocab_path, extra_vocab_sources)
    parser = CellParser(vocab)

    tables_out = []
    for name in args.tables.split(","):
        tex = (table_dir / f"{name}.tex").read_text(encoding="utf-8")
        conv = convert_table(tex, parser, papers_by_key)
        if conv:
            tables_out.append({"id": name, **conv})
        else:
            print(f"warning: could not convert table {name}")

    roadmap_out = parse_roadmap(Path(args.roadmap).read_text(encoding="utf-8"))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "papers.json").write_text(json.dumps(papers, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "tables.json").write_text(json.dumps(tables_out, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "roadmap.json").write_text(json.dumps(roadmap_out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"papers: {len(papers)}")
    print(f"tables: {len(tables_out)} ({', '.join(t['id'] for t in tables_out)})")
    print(f"roadmap root: {roadmap_out['name']!r} with {len(roadmap_out.get('children', []))} lanes")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
