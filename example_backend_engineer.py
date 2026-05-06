"""
Example: tailor a CV for a Senior Backend Engineer role at Acme Corp.

Copy this file, rename it (e.g. generate_cv_mycompany.py), and edit every
section to match your experience and the job description.

Run:
    python example_backend_engineer.py
"""

from cv_builder import CVBuilder

OUTPUT = "outputs/CV_Jane_Smith_Acme_Senior_Backend_Engineer.pdf"

cv = CVBuilder(OUTPUT)

# ── 1. Header ─────────────────────────────────────────────────────────────────
# Role title shown under your name — tailor to each JD.
cv.header("Senior Backend Engineer — Go, Kubernetes &amp; Distributed Systems")

# ── 2. Summary ────────────────────────────────────────────────────────────────
# ~3–4 sentences. Bold JD keywords. End with location + notice period.
cv.summary(
    "Senior backend engineer with <b>8+ years</b> building scalable, "
    "reliable distributed systems in <b>Go</b> and Python. Deep experience "
    "with <b>Kubernetes</b>, <b>Kafka</b>, and <b>AWS</b> — delivering "
    "microservices at <b>10M+ user scale</b> with <b>99.9% uptime</b>. "
    "Proven track record of owning systems end-to-end: design, delivery, "
    "observability, and on-call. Berlin-based, 1-month notice."
)

# ── 3. Skills ─────────────────────────────────────────────────────────────────
# Reorder languages to match the JD's preferred stack.
cv.skills([
    ("Languages",         "Go (primary), Python, C++"),
    ("Cloud & Infra",     "AWS (EKS, S3, IAM, multi-region), Kubernetes, Docker, Helm, Terraform"),
    ("Messaging",         "Kafka, Temporal — event-driven architecture at scale"),
    ("Databases",         "PostgreSQL, Redis, Elasticsearch"),
    ("Observability",     "Prometheus, Grafana, ELK stack, SLO/SLI/error budgets, distributed tracing"),
    ("Practices",         "Microservices, gRPC, REST, TDD, CI/CD, blameless postmortem culture"),
])

# ── 4. Work Experience ────────────────────────────────────────────────────────
# Most recent first. Lead bullet = strongest JD match.
# Use <b>bold</b> for JD keywords. Ground every claim in a number.
cv.job(
    "Acme Corp — Senior Backend Engineer",
    "Jan 2022 – Present | Berlin, Germany",
    "B2B SaaS platform — real-time data processing for 500+ enterprise customers.",
    [
        "Designed and owned the <b>event-driven ingestion pipeline</b> using "
        "<b>Kafka</b> and <b>Temporal</b>: processed <b>2M events/day</b> with "
        "guaranteed delivery, reducing data latency from 5 min to <b>under 10 s</b>.",

        "Migrated a monolith to <b>Kubernetes (EKS)</b>-based microservices using "
        "<b>Terraform</b> and Helm: enabled independent deployments and cut "
        "release cycle from 2 weeks to <b>2 days</b>.",

        "Defined <b>SLOs/SLIs</b> and error budgets for all critical services; "
        "built burn-rate alerting — achieving <b>99.9% uptime</b> over 12 months.",

        "Led <b>PostgreSQL schema migrations</b> zero-downtime across a 200M-row "
        "table; optimised slow queries — reduced p99 from <b>800 ms to 60 ms</b>.",
    ]
)

cv.job(
    "Beta Startup — Backend Engineer",
    "Jun 2018 – Dec 2021 | Remote",
    "Developer tooling SaaS — 50K active users.",
    [
        "Built core <b>Go</b> REST and <b>gRPC</b> APIs from scratch; introduced "
        "structured logging and distributed tracing — cut mean time to debug "
        "from hours to <b>under 15 minutes</b>.",

        "Introduced <b>TDD</b> and automated CI/CD (GitHub Actions): "
        "unit + integration test coverage from 20% to <b>85%</b>, "
        "eliminating a class of recurring production bugs.",
    ]
)

# ── 5. Education ──────────────────────────────────────────────────────────────
cv.education([
    (
        "MSc Computer Science",
        "Technical University of Berlin &nbsp;(2016–2018)",
        "Thesis: Distributed Consensus in Edge Networks"
    ),
    (
        "BSc Computer Engineering",
        "University of Example &nbsp;(2012–2016)",
        ""
    ),
])

# ── 6. Awards (optional — delete section if not applicable) ──────────────────
cv.awards([
    "1st place — Internal Hackathon, Acme Corp 2023",
    "Top 10% — Advent of Code 2022",
])

# ── 7. Render ─────────────────────────────────────────────────────────────────
cv.build()
