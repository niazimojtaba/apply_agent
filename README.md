# CV Generator

A lightweight Python toolkit for generating clean, ATS-friendly PDF CVs tailored to specific job descriptions — one script per application.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why

Most CV tools force you into rigid templates or online editors. This toolkit gives you **full control in plain Python**:

- One `profile.yaml` stores your personal details — edit once, used everywhere
- One script per job application — tailor bullets, reorder skills, adjust the title
- PDF output via [ReportLab](https://www.reportlab.com/) — no browser, no account, no cloud

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/cv-generator.git
cd cv-generator

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fill in your details
nano profile.yaml        # name, email, phone, LinkedIn, location

# 4. Copy the example and tailor it
cp example_backend_engineer.py generate_cv_mycompany.py
nano generate_cv_mycompany.py   # edit summary, skills, bullets

# 5. Generate
python generate_cv_mycompany.py
# → outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf
```

---

## Project Structure

```
cv-generator/
├── profile.yaml                    # your personal info (fill once)
├── cv_builder.py                   # rendering engine (don't edit)
├── example_backend_engineer.py     # example tailored script
├── requirements.txt
├── outputs/                        # generated PDFs go here (git-ignored)
└── README.md
```

---

## How It Works

### 1. `profile.yaml` — personal details

```yaml
name: "Jane Smith"
email: "jane@example.com"
phone: "+49 123 4567890"
location: "Berlin, Germany"
linkedin: "https://linkedin.com/in/janesmith"
accent_color: "1a5276"   # hex colour used for headings and bullets
```

### 2. Per-role script — tailored content

```python
from cv_builder import CVBuilder

cv = CVBuilder("outputs/CV_Jane_Smith_Acme_Engineer.pdf")

cv.header("Senior Backend Engineer — Go & Kubernetes")

cv.summary("Senior engineer with 8+ years building <b>distributed systems</b>…")

cv.skills([
    ("Languages",  "Go, Python, C++"),
    ("Cloud",      "AWS, Kubernetes, Terraform"),
    ("Databases",  "PostgreSQL, Redis"),
])

cv.job(
    "Acme Corp — Senior Backend Engineer",
    "2022–Present | Berlin",
    "B2B SaaS — 500 enterprise customers.",
    [
        "Designed <b>Kafka</b> ingestion pipeline processing <b>2M events/day</b>.",
        "Reduced p99 latency from <b>800 ms to 60 ms</b> via query optimisation.",
    ]
)

cv.education([("MSc Computer Science", "TU Berlin (2018–2020)", "")])
cv.awards(["1st place — Internal Hackathon 2023"])

cv.build()
```

### 3. Run it

```bash
python generate_cv_acme.py
# → outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf
```

---

## Tailoring Tips

### Match score before you write

Before tailoring, score the JD against your experience (0–100%). Only apply if ≥65%.

| Score | Signal |
|-------|--------|
| 85–100% | Strong fit — lead with JD keywords |
| 70–84%  | Good fit — address gaps honestly |
| 55–69%  | Stretch — apply, flag gaps upfront |
| < 55%   | Skip or apply only if very interested |

### Language order

Always list languages in the order the JD emphasises them:

```python
# Backend/infra role (Go preferred)
("Languages", "Go, Python, C++")

# ML/data role (Python preferred)
("Languages", "Python, Go, C++")
```

### Bold JD keywords

Wrap exact JD terms in `<b>…</b>` tags. ATS parsers and recruiters both scan for these:

```python
"Designed <b>event-driven architecture</b> using <b>Kafka</b> and <b>Temporal</b>…"
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
