# Awesome Self-Evolving Agent Safety

Project page and repository for **"Safety in Self-Evolving Agents: A Survey"** — a transition-centered study of how reusable influence persists, moves, and changes role across carriers in self-evolving agents, organized by the **SAVER** framework (`S×A → V→E→R`).

[![Stars](https://img.shields.io/github/stars/xaddwell/Awesome-Self-Evolving-Agent-Safety?style=flat&label=Stars&color=2563eb)](https://github.com/xaddwell/awesome-self-evolving-agent-safety)
[![Homepage](https://img.shields.io/badge/Homepage-xaddwell.github.io-blue)](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/)

## Paper

- **Title:** Safety in Self-Evolving Agents: A Survey
- **Authors:** Jiahao Chen, Zhou Feng, Oubo Ma, Yichen Yan, Ruixiao Lin, Hangtao Zhang, Linkang Du, Yiming Li, Hengyu An, Jun Liu, Junhao Li, Naen Xu, Mengyao Du, Yuanyi Song, Chunyi Zhou, Tianyu Du, Yuan Su, Zehao Jin, Qianli Ma, Leyi Qi, Yiming Wang, Zhihui Fu, Jun Wang, Zhe Ma, Yuwen Pu, Jinfeng Li, Shouling Ji
- **PDF:** [`assets/SAVER-Survey.pdf`](assets/SAVER-Survey.pdf)

## What Is SAVER?

Self-evolving agents turn observations, feedback, and execution traces into reusable state that shapes later behavior. SAVER analyzes this safety problem through one relation:

- **S · Substrate** — where does the reusable influence reside?
- **A · Adaptation** — how does its role change?
- **V · Violation** — which safety attribute fails to travel?
- **E · Exposure** — where does the failure become observable?
- **R · Response** — what can contain or repair it?

## Interactive Project Page

The page at [xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety](https://xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/) renders everything live from `papers.json`:

- corpus funnel (screened registry → unique works → coded pool → Figure 2 window);
- papers-per-year trend, SAVER taxonomy sunburst, SAVER flow sankey, record-origin donut, and terminal-family bars (ECharts);
- a clickable SAVER relation diagram;
- a searchable, collapsible paper index grouped by substrate lane and adaptation operation;
- a full **Paper Reader** ([`papers.html`](papers.html)) with multi-field filters.

## Repository Structure

```
.
├── index.html                  # Project page
├── papers.html                 # Paper Reader (search + filters)
├── papers.json                 # 619 coded records (generated)
├── stats.json                  # Corpus aggregates (generated)
├── assets/
│   └── SAVER-Survey.pdf        # Paper PDF
├── data/
│   └── saver_record_literature.csv   # Coding source of truth (same file that drives the manuscript Figure 2)
├── tools/
│   └── gen_papers_json.py      # CSV -> papers.json / stats.json generator
├── saver.bib                   # BibTeX entry
└── README.md
```

## Updating the Data

The coding CSV is the single source of truth. After updating it, regenerate the page data:

```bash
python3 tools/gen_papers_json.py --csv data/saver_record_literature.csv --out .
```

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

The page code in this repository is MIT-style free to adapt; the paper PDF, figure content, and coded data are derived from the survey manuscript and are provided for presentation and citation purposes. Contact the corresponding author (xaddwell@zju.edu.cn) for reuse beyond citation.
