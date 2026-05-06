# CV Generator

A lightweight Python toolkit for generating clean, ATS-friendly PDF CVs tailored to specific job descriptions — one script per application.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why

Most CV tools force you into rigid templates or online editors. This toolkit gives you **full control in plain Python**:

- One `profile.yaml` for personal details — fill in once
- One `base_resume.py` for your complete work history — write all your bullets once
- One script per application — cherry-pick and bold what fits each JD
- PDF output via [ReportLab](https://www.reportlab.com/) — no browser, no account, no cloud

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/cv-generator.git
cd cv-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fill in your personal details
nano profile.yaml          # name, email, phone, LinkedIn, location

# 4. Add your full work history
nano base_resume.py        # all your jobs, bullets, education, awards

# 5. Copy the example and tailor it to a specific JD
cp example_backend_engineer.py generate_cv_mycompany.py
nano generate_cv_mycompany.py

# 6. Generate
python3 generate_cv_mycompany.py
# → outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf
```

---

## Project Structure

```
cv-generator/
├── profile.yaml                    # personal info: name, email, phone, LinkedIn (git-ignored)
├── base_resume.py                  # your complete work history — write once, reuse everywhere
├── cv_builder.py                   # PDF rendering engine (no need to edit)
├── example_backend_engineer.py     # fully worked example showing the workflow
├── requirements.txt
├── outputs/                        # generated PDFs land here (git-ignored)
└── README.md
```

---

## How It Works — Three Layers

### Layer 1 — `profile.yaml` · Personal details

Fill this in once. Every script reads your name, contact info, and accent colour from here automatically.

```yaml
name: "Jane Smith"
email: "jane@example.com"
phone: "+49 123 4567890"
location: "Berlin, Germany"
linkedin: "https://linkedin.com/in/janesmith"
accent_color: "1a5276"     # hex colour for headings and bullet points
```

---

### Layer 2 — `base_resume.py` · Your complete history

Think of this as your **master resume** — every job you've held, every bullet you've ever written, all your education and awards. Nothing here is printed automatically; you import from it selectively in each script.

```python
# base_resume.py

SKILLS = {
    "languages":    "Go, Python, C++, Scala",
    "cloud":        "AWS (EKS, S3, IAM), Kubernetes, Docker, Helm, Terraform",
    "messaging":    "Kafka, Temporal — event-driven architecture at scale",
    "databases":    "PostgreSQL, Elasticsearch, Redis",
    "observability":"ELK stack, SLO/SLI/error budgets, distributed tracing",
}

JOBS = {
    "acme_senior": {
        "header":  "Acme Corp — Senior Backend Engineer",
        "period":  "Jan 2022 – Present | Berlin, Germany",
        "desc":    "B2B SaaS platform — 500+ enterprise customers.",
        "bullets": [
            # Write every bullet you could ever use for this role.
            # You'll pick the best ones per application.
            "Designed <b>Kafka</b> ingestion pipeline processing <b>2M events/day</b>…",
            "Migrated monolith to <b>Kubernetes (EKS)</b> — cut release cycle to <b>2 days</b>.",
            "Defined <b>SLOs/SLIs</b> and error budgets — <b>99.9% uptime</b>.",
            "Led <b>PostgreSQL</b> zero-downtime migrations on 200M-row table…",
        ],
    },
    # add more jobs…
}

EDUCATION = [
    ("MSc Computer Science", "TU Berlin (2016–2018)", "Thesis: Distributed Consensus…"),
    ("BSc Computer Engineering", "University of Example (2012–2016)", ""),
]

AWARDS = ["1st place — Hackathon 2023", "Top 10% — Advent of Code 2022"]
```

---

### Layer 3 — Per-role script · Tailored application

Copy `example_backend_engineer.py`, rename it, and select/reorder content from `base_resume.py` to match the specific JD. Bold the keywords the JD uses. Adjust the summary and title.

```python
# generate_cv_mycompany.py

from cv_builder import CVBuilder
import base_resume as base

cv = CVBuilder("outputs/CV_Jane_Smith_Acme_Engineer.pdf")

# Title tailored to this JD
cv.header("Senior Backend Engineer — Go, Kubernetes &amp; Distributed Systems")

# Summary rewritten for this role
cv.summary(
    "Senior engineer with <b>8+ years</b> building <b>distributed systems</b> "
    "in <b>Go</b>. Deep experience with <b>Kubernetes</b> and <b>Kafka</b> at "
    "<b>10M+ user scale</b>. Berlin-based, 1-month notice."
)

# Skills — reorder to match the JD's preferred stack
cv.skills([
    ("Languages", "<b>Go</b> (primary), Python, C++"),
    ("Cloud",     "<b>AWS</b>, <b>Kubernetes</b>, Terraform"),
    ("Databases", base.SKILLS["databases"]),   # reuse from base
])

# Jobs — import from base, pick only the most relevant bullets
acme = base.JOBS["acme_senior"]
cv.job(
    acme["header"], acme["period"], acme["desc"],
    [
        acme["bullets"][0],   # Kafka — JD asks for event-driven
        acme["bullets"][1],   # Kubernetes — JD asks for K8s
        acme["bullets"][2],   # SLO/uptime — JD asks for SRE
    ]
)

cv.education(base.EDUCATION)
cv.awards(base.AWARDS)
cv.build()
```

```bash
python3 generate_cv_mycompany.py
# → outputs/CV_Jane_Smith_MyCompany_Senior_Backend_Engineer.pdf
```

---

## Tailoring Tips

### Score the JD before writing

Compare the JD requirements to your experience and assign a score before writing a single word.

| Score | Signal |
|-------|--------|
| 85–100% | Strong fit — lead with JD keywords |
| 70–84%  | Good fit — address gaps honestly |
| 55–69%  | Stretch — apply, flag gaps upfront |
| < 55%   | Skip or apply only if very interested |

### Language order

Always list languages in the order the JD emphasises them — the recruiter's eye lands on the first word:

```python
# Backend/infra role (Go preferred)
("Languages", "Go, Python, C++")

# ML/data role (Python preferred)
("Languages", "Python, Go, C++")
```

### Bold JD keywords inline

Wrap exact JD terms in `<b>…</b>`. Both ATS parsers and recruiters scan for these:

```python
"Built <b>event-driven architecture</b> using <b>Kafka</b> and <b>Temporal</b>…"
```

### Ground every bullet in a number

Weak: `"Improved system performance."`  
Strong: `"Reduced p99 latency from <b>800 ms to 60 ms</b> serving <b>10M MAU</b>."`

---

## Output

PDFs are written to `outputs/`. The folder is git-ignored — your generated CVs stay local.

---

## Requirements

- Python 3.10+
- `reportlab >= 4.0.0`
- `PyYAML >= 6.0`

---

## License

MIT — use freely, attribution appreciated but not required.
