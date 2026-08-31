<div align="center">

# Safety in Self-Evolving Agents: A Survey

[![Website](https://img.shields.io/badge/Website-Project%20Page-blue.svg)](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Papers](https://img.shields.io/badge/Papers-625-blue.svg)](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/xaddwell/awesome-self-evolving-agent-safety/pulls)
[![GitHub stars](https://img.shields.io/github/stars/xaddwell/awesome-self-evolving-agent-safety?style=social)](https://github.com/xaddwell/awesome-self-evolving-agent-safety)

**A transition-centered survey of safety in self-evolving agents: how reusable influence persists, moves, and changes role across carriers — organized by the SAVER framework (`S×A → V→E→R`) over 625 coded papers.**

[[Website]](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/) · [[Paper Reader]](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html) · [[Paper (PDF)]](assets/SAVER-Survey.pdf)

</div>

## Authors

<div align="center">

<a href="https://xaddwell.github.io/" target="_blank" rel="noopener">Jiahao Chen</a><sup>1</sup>, Zhou Feng<sup>1</sup>, Oubo Ma<sup>1</sup>, Yichen Yan<sup>1</sup>, Ruixiao Lin<sup>1</sup>, Hangtao Zhang<sup>2</sup>, Linkang Du<sup>3</sup>, Yiming Li<sup>8</sup>, Hengyu An<sup>1</sup>, Jun Liu<sup>13</sup>, Junhao Li<sup>1</sup>, Naen Xu<sup>1</sup>, Mengyao Du<sup>4</sup>, Yuanyi Song<sup>5</sup>, Chunyi Zhou<sup>1</sup>, Tianyu Du<sup>1</sup>, Yuan Su<sup>1</sup>, Zehao Jin<sup>6</sup>, Qianli Ma<sup>7</sup>, Leyi Qi<sup>8</sup>, Yiming Wang<sup>1</sup>, Zhihui Fu<sup>2</sup>, Jun Wang<sup>2</sup>, Zhe Ma<sup>9</sup>, Yuwen Pu<sup>11</sup>, Jinfeng Li<sup>12</sup>, Shouling Ji<sup>1</sup>

<sup>1</sup>&nbsp;Zhejiang University &nbsp;·&nbsp; <sup>2</sup>&nbsp;Huazhong University of Science and Technology &nbsp;·&nbsp; <sup>3</sup>&nbsp;Xi'an Jiaotong University &nbsp;·&nbsp; <sup>4</sup>&nbsp;National University of Defense Technology &nbsp;·&nbsp; <sup>5</sup>&nbsp;Shanghai Jiaotong University &nbsp;·&nbsp; <sup>6</sup>&nbsp;Georgia Institute of Technology &nbsp;·&nbsp; <sup>7</sup>&nbsp;University of Science and Technology of China &nbsp;·&nbsp; <sup>8</sup>&nbsp;Nanyang Technological University &nbsp;·&nbsp; <sup>9</sup>&nbsp;OPPO Research Institute &nbsp;·&nbsp; <sup>11</sup>&nbsp;Chongqing University &nbsp;·&nbsp; <sup>12</sup>&nbsp;Alibaba Group &nbsp;·&nbsp; <sup>13</sup>&nbsp;Rakuten Group

✉ Correspondence: sji@zju.edu.cn

</div>

## Overview

Large language models remain fundamentally static: their parameters cannot adapt to novel tasks, evolving knowledge domains, or dynamic interaction contexts. Self-evolving agents break this bottleneck by turning observations, feedback, and execution traces into **reusable state** that shapes later behavior — memory consolidation, skill acquisition, workflow refinement, shared-state coordination, and model-side adaptation.

This capability changes the safety problem. When experience becomes reusable state, past events become future causes: information that was harmless in one context can later influence decisions with greater persistence, authority, or scope. **SAVER** analyzes this problem through one transition-centered relation:

| Field | Question | Content |
| ----- | -------- | ------- |
| **S · Substrate** | Where does the reusable influence reside? | Prompt context, memory, retrieval chunks, tool bindings, workflow rules, shared artifacts, adapters, policy state |
| **A · Adaptation** | How does its role change? | Seven operation families: `add`, `abstract`, `activate`, `modify`, `forget`, `propagate`, `migrate` |
| **V · Violation** | Which safety attribute fails to travel? | Provenance loss, authority escalation, scope widening, privacy breach, availability loss, budget exhaustion, missing audit, reversibility failure |
| **E · Exposure** | Where does the failure become observable? | Tool calls, model outputs, shared artifacts, governance audits, deletion requests |
| **R · Response** | What can contain or repair it? | Admission gates, migration checks, activation authorization, runtime guards, descendant rollback, deletion verification, contestability |

**Key insights.** (1) Many safety failures originate not from harmful information but from unsafe transitions that elevate the persistence, authority, or scope of legitimate state. (2) The field controls unsafe admission and visible failures well, but influence-lineage tracking across migration, propagation, and recovery remains fragmented. (3) Evaluation should move from endpoint metrics to lifecycle-level evidence that unsafe influence is traced, contained, and prevented from re-emerging after continued adaptation.

## Corpus

The coded pool follows the survey's systematic scoping protocol (see the paper's survey-protocol appendix):

| Stage | Count |
| ----- | ----: |
| Screened bibliographic records (14 June 2026 snapshot) | 583 |
| Unique registry works (4 duplicates canonicalized) | 579 |
| **Coded pool** (registry + 46 reviewed paper-card supplements) | **625** |
| Records in the Figure 2 window (2023 – 7 Aug 2026) | 524 |

## Taxonomy

All counts and links are driven by `papers.json`, generated from [`data/saver_record_literature.csv`](data/saver_record_literature.csv) — the same coding surface that drives the manuscript figures.

### Substrate families

| Family | Papers | Reader link |
| ------ | -----: | ----------- |
| Workflow (rules · planners · shared artifacts) | 293 | [open](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html?substrate=Workflow) |
| Memory (context · long-term · retrieval) | 195 | [open](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html?substrate=Memory) |
| Tools & Skills (bindings · skill libraries · MCP) | 99 | [open](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html?substrate=Tools%20%26%20Skills) |
| Model (parameters · adapters · policy) | 38 | [open](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html?substrate=Model) |

### Adaptation operations

`add` · `abstract` · `activate` · `modify` · `forget` · `propagate` · `migrate` — e.g., [propagate](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html?adaptation=Propagate), [migrate](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/papers.html?adaptation=Migrate).

### Terminal families

**Violation** — Provenance Loss · Authority Escalation · Privacy & Purpose · Persistent Descendants · Operational Integrity · Model Safety Regression
**Response** — Preventive Governance · Transition & Activation · Monitoring & Containment · Recovery & Contestability

## Interactive Project Page

[`index.html`](index.html) renders everything live from `papers.json` / `stats.json` / `tables.json` / `roadmap.json`:

- corpus funnel; papers-per-year trend (2023+ window); SAVER taxonomy sunburst; SAVER flow sankey; record-origin donut; terminal-family bars (ECharts, click → filtered Paper Reader);
- a clickable `S×A→V→E→R` diagram with per-field definitions;
- the **Literature Roadmap** in the paper's own layout and colors, with numbered reference links;
- the paper's **eight classification tables** converted from LaTeX to live HTML;
- a full **Paper Reader** ([`papers.html`](papers.html)) with search and multi-field filters.

## Repository Structure

```
.
├── index.html                  # Project page
├── papers.html                 # Paper Reader (search + filters)
├── papers.json                 # 625 coded records (generated)
├── stats.json                  # Corpus aggregates (generated)
├── tables.json                 # Classification tables (generated from LaTeX)
├── roadmap.json                # Roadmap tree (generated from LaTeX)
├── assets/
│   └── SAVER-Survey.pdf        # Paper PDF
├── data/
│   └── saver_record_literature.csv   # Coding source of truth
├── source/                     # Vendored LaTeX sources (tables + roadmap)
├── tools/
│   └── gen_papers_json.py      # CSV + LaTeX → JSON generator
├── saver.bib                   # BibTeX entry
├── CITATION.cff                # GitHub citation metadata
├── llms.txt                    # Repo summary for LLM agents
└── README.md
```

## Updating the Data

The coding CSV and the vendored LaTeX sources are the single sources of truth:

```bash
python3 tools/gen_papers_json.py
```

## Contribute

We welcome corrections and new papers. Please open an issue using the [Paper Submission](https://github.com/xaddwell/awesome-self-evolving-agent-safety/issues/new?template=paper-submission.md) template with the paper title, link, and your proposed SAVER coding (substrate / adaptation / outcome family). Changes are reconciled against `data/saver_record_literature.csv`, the same surface that drives the manuscript figures. For feedback on the survey itself, contact sji@zju.edu.cn.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=xaddwell/awesome-self-evolving-agent-safety&type=Date)](https://star-history.com/#xaddwell/awesome-self-evolving-agent-safety&Date)

## Citation

```bibtex
@article{chen2026saver,
  title={Safety in Self-Evolving Agents: A Survey},
  author={Chen, Jiahao and Feng, Zhou and Ma, Oubo and Yan, Yichen and Lin, Ruixiao and Zhang, Hangtao and Du, Linkang and Li, Yiming and An, Hengyu and Liu, Jun and Li, Junhao and Xu, Naen and Du, Mengyao and Song, Yuanyi and Zhou, Chunyi and Du, Tianyu and Su, Yuan and Jin, Zehao and Ma, Qianli and Qi, Leyi and Wang, Yiming and Fu, Zhihui and Wang, Jun and Ma, Zhe and Pu, Yuwen and Li, Jinfeng and Ji, Shouling},
  year={2026},
  note={Preprint}
}
```

## License

This repository is licensed under [CC BY-NC-SA 4.0](LICENSE) — the page code may be adapted freely with attribution, and the paper PDF, figure content, and coded data are provided for presentation and citation purposes. Contact the corresponding author for reuse beyond citation.
